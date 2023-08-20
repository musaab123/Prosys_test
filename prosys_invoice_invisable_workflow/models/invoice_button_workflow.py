from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'sale.order'

    