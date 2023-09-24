from odoo import api, fields, models, _
class SaleOrder(models.Model):
    _inherit = "sale.order"

    cash_payment = fields.Boolean('Cash')
    invisible_create_invoice = fields.Boolean(string="Invisible Create Invoice", compute="_compute_invisible_create_invoice")

    @api.depends('cash_payment')
    def _compute_invisible_create_invoice(self):
        for rec in self :
            rec.invisible_create_invoice = True
            if rec.cash_payment :
                rec.invisible_create_invoice = False
            elif self.user_has_groups('prosys_prmition_group.create_invoice_approval_custom'):
                rec.invisible_create_invoice = False


  

   