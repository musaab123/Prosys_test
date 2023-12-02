from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def _onchange_product_id_set_product_packaging(self):
        if self.product_id:
            packaging_ids = self.product_id.packaging_ids
            default_packaging = None

            for packaging_id in packaging_ids:
                if not default_packaging or packaging_id.qty < default_packaging.qty:
                    default_packaging = packaging_id

            if default_packaging:
                self.product_uom_qty = default_packaging.qty
                self.product_packaging_id = default_packaging
            else:
                self.product_uom_qty = 1
                self.product_packaging_id = False


