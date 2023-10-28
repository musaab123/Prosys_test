# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, date,timedelta as td

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    partner_number = fields.Integer("Partner Number")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    rent_contract_id = fields.Many2one('rental.contract', string="Rent Contract")
    from_date = fields.Date('From Date', related='rent_contract_id.date_from')
    from_hijri_date = fields.Date(string='Hijri Date')
    to_date = fields.Date('To Date', related='rent_contract_id.date_to')
    counted_days = fields.Integer('Days', readonly=True)
    statement_auto = fields.Text("Statement Auto")

    def action_post(self):
        res = super(AccountPayment, self).action_post()

        if self.statement_auto:
            for rec in self.move_id:
                for row in rec.invoice_line_ids:
                    row.write(
                        {
                            'statement_auto': self.statement_auto,
                        }
                    )

        return res

    @api.onchange('partner_id')
    def _get_contract_domain(self):
        if self.partner_id:
            return {'domain': {'rent_contract_id': [('partner_id', '=', self.partner_id.id)]}}

    @api.onchange('from_date', 'to_date', 'ref', 'rent_contract_id')
    def _onchange_from_date(self):
        if self.from_date and self.to_date:

            date_format = '%Y-%m-%d'
            date1 = datetime.strptime(str(self.from_date), date_format)
            date2 = datetime.strptime(str(self.to_date), date_format)

            delta = date2 - date1
            self.counted_days = delta.days

            self.statement_auto = ("paid amount from date "+str(self.from_date)+ " "+"to date "+" "+ str(self.to_date)+
                                   "\n in proportion to the duration of the contract days"+" "+ str(self.counted_days)+" "+"days")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    statement_auto = fields.Text("Statement Auto")