from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_packaging_qty = fields.Integer(string='Package Quantity')