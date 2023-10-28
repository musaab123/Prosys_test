# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from markupsafe import Markup
from odoo import api, fields, Command, models, _
from odoo.tools import float_round
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero, float_repr, float_compare, is_html_empty
from odoo.tools.misc import clean_context, format_date

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    partner_id = fields.Many2one('res.partner', string="Partner")
    partner_number =  fields.Integer('Partner Number')
    rent_contract_id = fields.Many2one('rental.contract', string="Contract")
    building_units = fields.Many2one('product.template', string='Building Units', related='rent_contract_id.building_unit')
    statement = fields.Text('Statement')
    paid_by_partner = fields.Selection(
        string='Pay by Partner',
        selection=[('normal', 'Normal'), ('paid_by_partner', 'Pay by Partner')], default='normal')

    @api.onchange('partner_id')
    def _get_contract_domain(self):
        if self.partner_id:
            return {'domain': {'rent_contract_id': [('partner_id', '=', self.partner_id.id)]}}


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    partner_id = fields.Many2one('res.partner', string="Partner", store=True)
    partner_number = fields.Integer('Partner Number')
    rent_contract_id = fields.Many2one('rental.contract', string="Contract", store=True)
    building_units = fields.Many2one('product.template', string='Building Units', store=True)
    statement = fields.Text('Statement', store=True)

    @api.model_create_multi
    def create(self, vals):
        active_id = self.env.context.get('active_id')
        res = super(HrExpenseSheet, self).create(vals)
        expense_id = self.env['hr.expense'].search([('id', '=', active_id)])
        expense_sheet_id = self.env['hr.expense.sheet'].search([('id', '=', res.id)])
        expense_sheet_id.write(
            {
                'partner_id': expense_id.partner_id.id,
                'partner_number': expense_id.partner_number,
                'rent_contract_id': expense_id.rent_contract_id.id,
                'building_units': expense_id.building_units.id,
                'statement': expense_id.statement,
            }
        )
        return res

    @api.onchange('expense_line_ids')
    def get_expense_line_ids(self):
        for rec in self.expense_line_ids:
            self.write(
                {
                    'partner_id': rec.partner_id.id,
                    'partner_number': rec.partner_number,
                    'rent_contract_id': rec.rent_contract_id.id,
                    'building_units': rec.building_units.id,
                    'statement': rec.statement,
                }
            )

    def action_sheet_move_create(self):
        res = super(HrExpenseSheet, self).action_sheet_move_create()
        expense_id = self.env['hr.expense'].search([('sheet_id', '=', self.id)], limit=1)
        if expense_id.statement:
            for rec in self.account_move_id:
                for row in rec.invoice_line_ids:
                    row.write(
                        {
                            'statement_auto': expense_id.statement,
                        }
                    )

        return res
