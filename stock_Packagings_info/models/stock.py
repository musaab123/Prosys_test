from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, float_round


class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'

    # product_packaging_qty = fields.Float(
    #     string="Packaging Quantity",
    #     store=True, readonly=False, precompute=True)
    



class CustomStockMove(models.Model):
    _inherit = 'stock.move'
    
    product_packaging_qty = fields.Float(
        string="Packaging Quantity",
        compute='_compute_product_packaging_qty',
        store=True, readonly=False, precompute=True)
    
    qty = fields.Float(
        string=" Packaging Unit Qty",
        related='product_packaging_id.qty',
        store=True, readonly=False, precompute=True)
    
   
    done_qty_package = fields.Float(
        string="Done Packing Packing",
        compute='_compute_product_packag_done',
        store=True, readonly=False, precompute=True)
    

    

    @api.depends('product_packaging_id', 'product_uom', 'quantity_done')
    def _compute_product_packag_done(self):
        for line in self:
            if not line.product_packaging_id:
                line.done_qty_package = False
            else:
                packaging_uom = line.product_packaging_id.product_uom_id
                packaging_uom_qty = line.product_uom._compute_quantity(line.quantity_done, packaging_uom)
                line.done_qty_package = float_round(
                    packaging_uom_qty / line.product_packaging_id.qty,
                    precision_rounding=packaging_uom.rounding)
                

    

    
    

    @api.depends('product_packaging_id', 'product_uom', 'product_uom_qty')
    def _compute_product_packaging_qty(self):
        for line in self:
            if not line.product_packaging_id:
                line.product_packaging_qty = False
            else:
                packaging_uom = line.product_packaging_id.product_uom_id
                packaging_uom_qty = line.product_uom._compute_quantity(line.product_uom_qty, packaging_uom)
                line.product_packaging_qty = float_round(
                    packaging_uom_qty / line.product_packaging_id.qty,
                    precision_rounding=packaging_uom.rounding)
