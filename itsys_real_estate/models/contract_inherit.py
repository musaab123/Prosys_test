# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, date,timedelta as td

class contractInh(models.Model):
    _inherit = 'rental.contract'

    periodicity = fields.Selection(selection_add=[
        ('midterm', 'midterm'),
          ('quarterly', 'quarterly'),
    ], ondelete={'midterm': 'set default', 'quarterly':'set default'})

    contract_time = fields.Integer(string="Contract duration on days", readonly=True)

    @api.onchange('date_from', 'date_to')
    def calculate_contract_days(self):
        date_format = '%Y-%m-%d'
        if self.date_from and self.date_to:
            date1 = datetime.strptime(str(self.date_from), date_format)
            date2 = datetime.strptime(str(self.date_to), date_format)

            delta = date2 - date1
            self.write(
                {
                    'contract_time': delta.days,
                }
            )


    # periodicity = fields.Selection([('days', 'Days'), ('weeks', 'Weeks'),
    #                                         ('months', 'Months'), ('years', 'Years'), ],
    #                                        string='Recurrence', required=True,
    #                                        help="Invoice automatically repeat at specified interval",
    #                                        default='months', tracking=True)


class contractCancel(models.Model):
    _name = 'contract.cancel'

    name = fields.Char('Name')
    rent_contract_id = fields.Many2one('rental.contract', string='Contract', domain=[('state', '=', 'confirmed')])
    tenant_id = fields.Many2one('res.partner', 'Tenant', related='rent_contract_id.partner_id')
    date_from = fields.Date('Date From', related='rent_contract_id.date_from')
    date_to = fields.Date('Date From', related='rent_contract_id.date_to')
    cancellation_date = fields.Date('Cancellation Date', default=fields.Datetime.now())
    contract_duration = fields.Integer('Contract Duration', related='rent_contract_id.contract_time')
    actual_duration = fields.Integer('Actual Duration', readonly=True)
    cancel_reason = fields.Text('Cancellation Reason')
    ref = fields.Text('Ref')
    statement = fields.Text('Statement')
    state = fields.Selection([('draft', 'Draft'),('confirmed', 'Confirmed')], default='draft')
    gain_loss_amount = fields.Float('Gain/Loss Amount')
    gain_loss_type = fields.Selection([('loss', 'Loss'), ('gain', 'Gain')])
    cancel_line_ids = fields.One2many('contract.cancel.line', 'cancel_id')

    @api.onchange('cancellation_date', 'rent_contract_id')
    def calculate_days(self):
        date_format = '%Y-%m-%d'
        if self.date_from and self.date_to and self.cancellation_date:
            date1 = datetime.strptime(str(self.date_from), date_format)
            date2 = datetime.strptime(str(self.cancellation_date), date_format)

            delta = date2 - date1
            self.write(
                {
                    'actual_duration': delta.days,
                }
            )
        if self.rent_contract_id:
            self.write(
                {
                    'name': self.rent_contract_id.name+"/"+ self.tenant_id.name,
                }
            )

    def set_to_draft(self):
        self.cancel_line_ids.write(
            {
                'state': 'draft',
            }
        )

    def calculate_details(self):
        actual_val = 0
        if self.contract_duration:
            each = self.rent_contract_id.amount_total/self.contract_duration
            actual_val = each * self.actual_duration

        print("actual val", actual_val)
        if self.rent_contract_id:
            cancel_line_id = self.env['contract.cancel.line']
            cancel_line_id.create(
                {
                    'cancel_id': self.id,
                    'real_estate_code': self.rent_contract_id.unit_code,
                    'real_estate_name': self.rent_contract_id.building_unit.name,
                    'contract_value': self.rent_contract_id.amount_total,
                    'actual_value': actual_val,
                    'cancelled_amount': self.rent_contract_id.amount_total - actual_val,
                }
            )

    def action_confirm(self):
        self.write(
            {
                'state': 'confirmed',
            }
        )
        self.rent_contract_id.action_cancel()

class contractCancelLine(models.Model):
    _name = 'contract.cancel.line'

    real_estate_code = fields.Char('Real Estate Code')
    real_estate_name = fields.Char('Real Estate Name')
    contract_value = fields.Float('Contract Value')
    contract_tax = fields.Float('Contract Tax')
    actual_value = fields.Float('Actual Value')
    actual_tax = fields.Float('Actual Tax')
    cancelled_amount = fields.Float('Cancelled Amount')
    cancelled_tax = fields.Float('Cancelled Tax')
    total = fields.Float('Total')
    paid = fields.Float('Paid')
    balance = fields.Float('Balance')
    cancel_id = fields.Many2one('contract.cancel')