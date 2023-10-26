from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    old_barcode = fields.Char(string='Old Barcode', help='Old barcode for the product', index=True, copy=False)
    
