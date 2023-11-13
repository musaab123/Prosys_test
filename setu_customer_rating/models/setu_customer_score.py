# -*- coding: utf-8 -*-

import json
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


class SetuCustomerScore(models.Model):
    _name = 'setu.customer.score'
    _description = 'Customer Score'
    _rec_name = 'partner_id'

    pre_sale_orders_canceled_score = fields.Integer(string="Score For Percentage of pre-sale orders canceled")
    total_score = fields.Integer(string="Total Score", group_operator=False)

    max_available_score = fields.Integer(compute='_compute_max_available_score', string="Max Available Score")
    partner_score = fields.Integer(string="Score", group_operator=False)
    avg_monthly_sales_score = fields.Integer(string="Score For Average Monthly Sales Count")
    avg_monthly_refund_score = fields.Integer(string="Score For Average monthly sales refunds Count")
    qty_invoice_paid_score = fields.Integer(string="Score For Quantity of Invoices paid after the due date Count")
    amount_invoice_paid_score = fields.Integer(string="Score For Amount of Invoices paid after the due date Count")
    qty_invoices_due_after_60_days_score = fields.Integer(
        string="Score For Quantity of Invoices due after X days Count")
    amount_invoices_due_after_60_days_score = fields.Integer(
        string="Score For Amount of Invoices due after X days Count")
    average_payment_days_score = fields.Integer(string="Score For Average payment days in your purchase history Count")

    partner_rating_text = fields.Text(compute='_compute_rating_text', string='Rating')
    avg_monthly_sales_score_text = fields.Text(compute='_compute_avg_monthly_sales_score',
                                               string="Score For Average Monthly Sales")
    avg_monthly_refund_score_text = fields.Text(compute='_compute_avg_monthly_refund_score_text',
                                                string="Score For Average monthly sales refunds")
    qty_invoice_paid_score_text = fields.Text(compute='_compute_qty_invoice_paid_score',
                                              string="Score For Quantity of Invoices paid after the due date")
    amount_invoice_paid_score_text = fields.Text(compute='_compute_amount_invoice_paid_score',
                                                 string="Score For Amount of Invoices paid after the due date")
    qty_invoices_due_after_60_days_score_text = fields.Text(compute='_compute_qty_invoices_due_after_60_days_score',
                                                            string="Score For Quantity of Invoices due after X days")
    amount_invoices_due_after_60_days_score_text = fields.Text(
        compute='_compute_amount_invoices_due_after_60_days_score',
        string="Score For Amount of Invoices due after X days")
    average_payment_days_score_text = fields.Text(compute='_compute_average_payment_days_score',
                                                  string="Score For Average payment days in your purchase history")

    partner_id = fields.Many2one('res.partner', string='Customer')
    customer_rating_id = fields.Many2one('setu.customer.rating', string="Rating")
    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=False)

    sale_ids = fields.Many2many('sale.order', 'average_sale_rel', 'score_id', 'sale_id')
    canceled_pre_orders = fields.Many2many('sale.order', 'customer_score_canceled_sales_rel', 'score_id', 'sale_id')
    invoice_done_after_due_date_ids = fields.Many2many('account.move', 'customer_score_paid_after_due_invoice_rel',
                                                       'score_id', 'invoice_id')
    invoices_due_after_60_days = fields.Many2many('account.move', 'customer_score_unpaid_after_60_days_invoice_rel',
                                                  'score_id', 'invoice_id')
    credit_notes = fields.Many2many('account.move', 'customer_score_refund_invoice_rel', 'score_id', 'invoice_id')

    def _compute_max_available_score(self):
        for record_id in self:
            max_rule = self.env['setu.customer.rating'].search(
                [('company_id', '=', self.customer_rating_id.company_id.id)], order='to_score desc', limit=1)
            record_id.max_available_score = max_rule.to_score

    def _compute_rating_text(self):
        for cs in self:
            customer_rating_id = self.customer_rating_id
            if customer_rating_id:
                rule_widget_vals = {'title': customer_rating_id.rating,
                                    'is_rating': True,
                                    'content': f"As Customer's total score is between {customer_rating_id.from_score} and {customer_rating_id.to_score}, Customer rating is {customer_rating_id.rating}."}
                cs.partner_rating_text = json.dumps(rule_widget_vals)
            else:
                cs.partner_rating_text = False

    def _compute_avg_monthly_sales_score(self):
        for record_id in self:
            score = self.avg_monthly_sales_score
            score_configuration_line_price_id = self.env['setu.score.configuration.line.price'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'avg_monthly_sales'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.avg_monthly_sales_score,
                                'is_rating': False,
                                'content': f"As Customer's Average monthly spend is between {score_configuration_line_price_id.from_price} and {score_configuration_line_price_id.to_price}, Average Monthly Sales score is {score}."}
            record_id.avg_monthly_sales_score_text = json.dumps(rule_widget_vals)

    def _compute_avg_monthly_refund_score_text(self):
        for record_id in self:
            score = self.avg_monthly_refund_score
            score_configuration_line_percentage_id = self.env['setu.score.configuration.line.percentage'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'avg_monthly_refund'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.avg_monthly_refund_score,
                                'is_rating': False,
                                'content': f"As customer's Average monthly sales refund percentage is between {score_configuration_line_percentage_id.from_percentage} and {score_configuration_line_percentage_id.to_percentage}, Score For Average monthly sales refunds is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']
            record_id.avg_monthly_refund_score_text = json.dumps(rule_widget_vals)

    def _compute_qty_invoice_paid_score(self):
        for record_id in self:
            score = self.qty_invoice_paid_score
            score_configuration_line_qty_id = self.env['setu.score.configuration.line.qty'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'qty_invoice_paid'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.qty_invoice_paid_score,
                                'is_rating': False,
                                'content': f"As customer's quantity of invoices paid after due date is between {score_configuration_line_qty_id.from_quantity} and {score_configuration_line_qty_id.to_quantity}, Score For Quantity of Invoices paid after the due date is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']

            record_id.qty_invoice_paid_score_text = json.dumps(rule_widget_vals)

    def _compute_amount_invoice_paid_score(self):
        for record_id in self:
            score = self.amount_invoice_paid_score
            score_configuration_line_price_id = self.env['setu.score.configuration.line.price'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'amt_invoice_paid'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.amount_invoice_paid_score,
                                'is_rating': False,
                                'content': f"As Customer's amount of Invoices paid after the due date is between {score_configuration_line_price_id.from_price} and {score_configuration_line_price_id.to_price}, score for amount of invoices paid after the due date is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']

            record_id.amount_invoice_paid_score_text = json.dumps(rule_widget_vals)

    def _compute_qty_invoices_due_after_60_days_score(self):
        for record_id in self:
            score = self.qty_invoices_due_after_60_days_score
            score_configuration_line_qty_id = self.env['setu.score.configuration.line.qty'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'qty_invoice_due'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.qty_invoices_due_after_60_days_score,
                                'is_rating': False,
                                'content': f"As customer's quantity of invoices due after X days is between {score_configuration_line_qty_id.from_quantity} and {score_configuration_line_qty_id.to_quantity}, score for quantity of invoices due after X days is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']
            record_id.qty_invoices_due_after_60_days_score_text = json.dumps(rule_widget_vals)

    def _compute_amount_invoices_due_after_60_days_score(self):
        for record_id in self:
            score = self.amount_invoices_due_after_60_days_score
            score_configuration_line_price_id = self.env['setu.score.configuration.line.price'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'amt_invoice_due'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.amount_invoices_due_after_60_days_score,
                                'is_rating': False,
                                'content': f"As customer's amount of invoices due after X days is between {score_configuration_line_price_id.from_price} and {score_configuration_line_price_id.to_price}, score For amount of invoices due after X days is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']

            record_id.amount_invoices_due_after_60_days_score_text = json.dumps(rule_widget_vals)

    def _compute_average_payment_days_score(self):
        for record_id in self:
            score = self.average_payment_days_score
            score_configuration_line_qty_id = self.env['setu.score.configuration.line.qty'].search(
                [('pre_score', '=', score), ('score_conf_id.calculation_formula', '=', 'avg_payment_days'),
                 ('score_conf_id.company_id', '=', record_id.company_id.id)], limit=1)
            rule_widget_vals = {'title': self.average_payment_days_score,
                                'is_rating': False,
                                'content': f"As customer's average payment days in their purchase history is between {score_configuration_line_qty_id.from_quantity} and {score_configuration_line_qty_id.to_quantity}, score for average payment days in their purchase history is {score}."}
            if score == 0:
                rule_widget_vals['content'] = "Customer has no paid invoices or " + rule_widget_vals['content']

            record_id.average_payment_days_score_text = json.dumps(rule_widget_vals)

    def get_queries(self):
        return 'set_customer_scores_no_pos', 'set_document_ids_no_pos'

    def name_get(self):
        result = []
        for r in self:
            text = r.partner_id and r.company_id and r.partner_id.name + ' - ' + r.company_id.name
            if text:
                result.append((r.id, text))
        if not result:
            return super(SetuCustomerScore, self).name_get()
        return result

    @api.model
    def run_customer_score_cron(self):
        companies_to_evaluate = []
        date_today = date.today()
        company_ids = self.env['res.company'].sudo().search([])
        for company_id in company_ids:
            score_configuration_ids = self.env['setu.score.configuration'].sudo().search(
                [('company_id', '=', company_id.id)])
            total_max_score = 0
            for score_configuration_id in score_configuration_ids:
                score1 = max(
                    score_configuration_id.score_conf_line_price_ids and score_configuration_id.score_conf_line_price_ids.mapped(
                        'pre_score') or [0])
                score2 = max(
                    score_configuration_id.score_conf_line_percentage_ids and score_configuration_id.score_conf_line_percentage_ids.mapped(
                        'pre_score') or [0])
                score3 = max(
                    score_configuration_id.score_conf_line_qty_ids and score_configuration_id.score_conf_line_qty_ids.mapped(
                        'pre_score') or [0])
                total = score3 + score2 + score1
                total_max_score += total
            if total_max_score != 100:
                message = 'Sum of maximum scores of individual rules is not 100. Customer rating evaluation for selected company is aborted.'
                company_id.banner_message = message
                company_id.customer_rating_calculated = False
            else:
                companies_to_evaluate.append(company_id.id)
                company_id.customer_rating_calculated = True
                company_id.banner_message = f'Customer Rating evaluation was done on {date_today}.'

        if companies_to_evaluate:
            self._cr.execute(f"select * from create_customer_score_records(array{companies_to_evaluate})")
            days = int(
                self.env['ir.config_parameter'].sudo().get_param('setu_customer_rating.customer_score_days')) or 365
            invoice_days = int(
                self.env['ir.config_parameter'].sudo().get_param('setu_customer_rating.past_days_for_invoice')) or 60
            invoice_due_date_limit = date.today() - relativedelta(days=invoice_days)
            date_limit = str(date.today() - relativedelta(days=days))
            months = int(days / 30)
            if months == 0:
                months = 1
            score_conf_avg_sales_amt_id = self.env.ref('setu_customer_rating.score_conf_avg_sales_amt').id
            score_conf_avg_monthly_sales_refund_id = self.env.ref(
                'setu_customer_rating.score_conf_avg_monthly_sales_refund').id
            score_conf_qty_invoice_paid_after_due_id = self.env.ref(
                'setu_customer_rating.score_conf_qty_invoice_paid_after_due').id
            score_conf_amt_invoice_paid_after_due_id = self.env.ref(
                'setu_customer_rating.score_conf_amt_invoice_paid_after_due').id
            score_conf_qty_invoice_paid_after_x_days_id = self.env.ref(
                'setu_customer_rating.score_conf_qty_invoice_paid_after_x_days').id
            score_conf_amt_invoices_due_after_x_days_id = self.env.ref(
                'setu_customer_rating.score_conf_amt_invoices_due_after_x_days').id
            score_conf_avg_payment_days_id = self.env.ref('setu_customer_rating.score_conf_avg_payment_days').id

            q1, q2 = self.get_queries()
            self._cr.execute("Select * from %s(%s,'%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s)" % (q1,
                                                                                         f'array{companies_to_evaluate}',
                                                                                         date_limit,
                                                                                         months,
                                                                                         invoice_due_date_limit,
                                                                                         score_conf_avg_sales_amt_id,
                                                                                         score_conf_avg_monthly_sales_refund_id,
                                                                                         score_conf_qty_invoice_paid_after_due_id,
                                                                                         score_conf_amt_invoice_paid_after_due_id,
                                                                                         score_conf_qty_invoice_paid_after_x_days_id,
                                                                                         score_conf_amt_invoices_due_after_x_days_id,
                                                                                         score_conf_avg_payment_days_id))

            self._cr.execute(
                f"select * from {q2}(array{companies_to_evaluate},'{date_limit}','{invoice_due_date_limit}')")
            self._cr.execute(f"select * from update_rating_data(array{companies_to_evaluate})")
            manage_history_query = f""" with crt as
               (
               Select 
                    SPLIT_PART(ip.res_id,',',2)::integer as partner_id,
                   --case when substring(ip.res_id from 13) != '' then substring(ip.res_id from 13)::integer else null::integer end as partner_id,
                   ip.company_id,
                   SPLIT_PART(ip.value_reference,',',2)::integer as current_rating,
                   --case when substring(ip.value_reference FROM 22) != '' then substring(ip.value_reference FROM 22)::integer else null::integer end as current_rating,
                   coalesce((
                       Select current_customer_rating_id from setu_partner_rating_history 
                       where substring(ip.res_id from 13) != '' and
                       partner_id =  substring(ip.res_id from 13)::int and
                       company_id = ip.company_id
                       order by date_changed desc limit 1

                   ),null)as previous_rating,
                    (select now()::timestamp without time zone) as date_changed
               from 
               ir_property ip
               where
               ip.company_id = any(array{companies_to_evaluate}) and
               ip.fields_id = (SELECT imf.id FROM ir_model_fields imf WHERE name = 'customer_rating_id' AND model_id = (SELECT m.id FROM ir_model m WHERE m.model = 'res.partner')))

               Insert into setu_partner_rating_history(partner_id, company_id, current_customer_rating_id, previous_customer_rating_id, date_changed)
               select * from crt where current_rating is not null and current_rating != coalesce(previous_rating,0);
               """
            self._cr.execute(manage_history_query)
            return True
        return False
