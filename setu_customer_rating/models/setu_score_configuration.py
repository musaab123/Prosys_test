# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SetuScoreConfiguration(models.Model):
    _name = 'setu.score.configuration'
    _description = 'Score Configuration'

    name = fields.Char(string="Rule")

    calculation_based_on = fields.Selection(
        [('price', 'Price'), ('percentage', 'Percentage'), ('quantity', 'Quantity')], required=True,
        string="Calculation Based On")
    calculation_formula = fields.Selection([('avg_monthly_sales', 'avg_monthly_sales'),
                                            ('avg_monthly_refund', 'avg_monthly_refund'),
                                            ('qty_invoice_paid', 'qty_invoice_paid'),
                                            ('amt_invoice_paid', 'amt_invoice_paid'),
                                            ('qty_invoice_due', 'qty_invoice_due'),
                                            ('amt_invoice_due', 'amt_invoice_due'),
                                            ('avg_payment_days', 'avg_payment_days')], required=True,
                                        string="Calculation Formula")

    company_id = fields.Many2one('res.company', string="Company")

    score_conf_line_price_ids = fields.One2many('setu.score.configuration.line.price', 'score_conf_id')
    score_conf_line_percentage_ids = fields.One2many('setu.score.configuration.line.percentage', 'score_conf_id')
    score_conf_line_qty_ids = fields.One2many('setu.score.configuration.line.qty', 'score_conf_id')

    @api.constrains('score_conf_line_price_ids')
    def price_validations(self):
        total_lines = self.score_conf_line_price_ids
        for line in total_lines:
            rules = line.sudo().search([('score_conf_id', '=', line.score_conf_id.id)])
            if rules.filtered(lambda rule: rule.id != line.id and rule.pre_score == line.pre_score):
                raise ValidationError(_('Same Pre-Score can not be applied to new rule.'))
            if line.from_price > line.to_price:
                raise ValidationError(_("'From Price' must be less than 'To Price'"))
            if rules.filtered(lambda rule: rule.id != line.id).filtered(
                    lambda rule: (rule.from_price < line.from_price
                                  and
                                  rule.to_price > line.to_price)
                                 or
                                 (rule.from_price > line.from_price
                                  and
                                  rule.to_price < line.to_price)
                                 or
                                 line.from_price <= rule.from_price <= line.to_price <= rule.to_price
                                 or
                                 rule.from_price <= line.from_price <= rule.to_price <= line.from_price):
                raise ValidationError(_("Rule's price range is conflicting with other rules."))

    @api.constrains('score_conf_line_percentage_ids')
    def percentage_validations(self):
        total_lines = self.score_conf_line_percentage_ids
        for line in total_lines:
            rules = line.sudo().search([('score_conf_id', '=', line.score_conf_id.id)])
            if rules.filtered(lambda rule: rule.id != line.id and rule.pre_score == line.pre_score):
                raise ValidationError(_('Same Pre-Score can not be applied to new rule.'))
            if line.from_percentage > line.to_percentage:
                raise ValidationError(_("'From Percentage' must be less than 'To Percentage'"))
            if rules.filtered(lambda rule: rule.id != line.id).filtered(
                    lambda rule: rule.from_percentage < line.from_percentage
                                 and
                                 rule.to_percentage > line.to_percentage
                                 or
                                 rule.from_percentage > line.from_percentage
                                 and
                                 rule.to_percentage < line.to_percentage
                                 or
                                 line.from_percentage <= rule.from_percentage <= line.to_percentage <= rule.to_percentage
                                 or
                                 rule.from_percentage <= line.from_percentage <= rule.to_percentage <= line.from_percentage):
                raise ValidationError(_("Rule's price range is conflicting with other rules."))

    @api.constrains('score_conf_line_qty_ids')
    def qty_validations(self):
        total_lines = self.score_conf_line_qty_ids
        for line in total_lines:
            rules = line.sudo().search([('score_conf_id', '=', line.score_conf_id.id)])
            if rules.filtered(lambda rule: rule.id != line.id and rule.pre_score == line.pre_score):
                raise ValidationError(_('Same Pre-Score can not be applied to new rule.'))
            if line.from_quantity > line.to_quantity:
                raise ValidationError(_("'From Quantity' must be less than 'To Quantity'"))
            if rules.filtered(lambda rule: rule.id != line.id).filtered(
                    lambda rule: rule.from_quantity < line.from_quantity
                                 and
                                 rule.to_quantity > line.to_quantity
                                 or
                                 rule.from_quantity > line.from_quantity
                                 and
                                 rule.to_quantity < line.to_quantity
                                 or
                                 line.from_quantity <= rule.from_quantity <= line.to_quantity <= rule.to_quantity
                                 or
                                 rule.from_quantity <= line.from_quantity <= rule.to_quantity <= line.from_quantity):
                raise ValidationError(_("Rule's price range is conflicting with other rules."))

    def create_rules(self, company_id):
        avg_monthly_sales = self.search([('calculation_formula', '=', 'avg_monthly_sales')], limit=1)

        avg_monthly_refund = self.search([('calculation_formula', '=', 'avg_monthly_refund')],
                                        limit=1)
        qty_invoice_paid = self.search([('calculation_formula', '=', 'qty_invoice_paid')], limit=1)
        amt_invoice_paid = self.search([('calculation_formula', '=', 'amt_invoice_paid')], limit=1)
        qty_invoice_due = self.search([('calculation_formula', '=', 'qty_invoice_due')], limit=1)
        amt_invoice_due = self.search([('calculation_formula', '=', 'amt_invoice_due')], limit=1)
        avg_payment_days = self.search([('calculation_formula', '=', 'avg_payment_days')], limit=1)
        confs = (
                avg_monthly_sales + avg_monthly_refund + qty_invoice_paid + amt_invoice_paid + qty_invoice_due + amt_invoice_due + avg_payment_days)

        for conf in confs:
            new_conf = conf.copy()
            new_conf.company_id = company_id
            for line in conf.score_conf_line_percentage_ids:
                new_line = line.copy()
                new_line.score_conf_id = new_conf
            for line in conf.score_conf_line_price_ids:
                new_line = line.copy()
                new_line.score_conf_id = new_conf
            for line in conf.score_conf_line_qty_ids:
                new_line = line.copy()
                new_line.score_conf_id = new_conf
        company = self.env['setu.customer.rating.company'].create({
            'company_id': company_id.id
        })
        self.env['setu.customer.rating'].with_context(let_me_create=True).create({
            'company_id': company_id.id,
            'from_score': 0,
            'to_score': 69,
            'rating': 'C',
            'crc_id': company.id
        })
        self.env['setu.customer.rating'].with_context(let_me_create=True).create({
            'company_id': company_id.id,
            'from_score': 70,
            'to_score': 79,
            'rating': 'B',
            'crc_id': company.id
        })
        self.env['setu.customer.rating'].with_context(let_me_create=True).create({
            'company_id': company_id.id,
            'from_score': 80,
            'to_score': 89,
            'rating': 'A',
            'crc_id': company.id
        })

        self.env['setu.customer.rating'].with_context(let_me_create=True).create({
            'company_id': company_id.id,
            'from_score': 90,
            'to_score': 100,
            'rating': 'AAA',
            'crc_id': company.id
        })
