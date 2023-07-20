# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'
    
    discount_amt = fields.Float('Discount', store=True)

    def _select(self):
        return super()._select() + ", line.discount_amt as discount_amt"
