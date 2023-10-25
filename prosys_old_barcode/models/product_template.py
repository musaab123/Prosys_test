from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(related='product_variant_ids.barcode_ids', readonly=False)

    @api.onchange('barcode_ids')
    def _onchange_lines(self):
        if len(self.barcode_ids) > 1:
            raise UserError("You can only add one Barcode to this product.")
