from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    conductor_ids = fields.Many2many(
        'hr.employee',
        'partner_employee_rel',
        'partner_id',
        'employee_id',
        string='Conductor'
    )


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    conductor_ids = fields.Many2many(
        'hr.employee',
        'payment_employee_rel',
        'payment_id',
        'employee_id',
        string='Conductor'
    )

    @api.onchange('conductor_ids')
    def add_conductors_to_ref(self):
        names = ""
        for conductor in self.conductor_ids:
            names += " __ " + conductor.name
        if self.ref:
            self.ref = self.ref.split(' __ ')[0] + names

class AcoountMove(models.Model):
    _inherit = 'account.move'

    conductor_ids = fields.Many2many(
        'hr.employee',
        'partner_employee_rel_test',
        'partner_id',
        'employee_id',
        readonly=True,
        string='Conductor'
    )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # sale_id = fields.Many2one('sale.order','Sale Order')
    conductor_ids = fields.Many2many(
        'hr.employee',
        'partner_employee_rel_sale',
        'partner_id',
        'employee_id',
        string='Conductor',
        
    )



    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['conductor_ids'] = [(6,0,self.conductor_ids.ids)]

        return invoice_vals



