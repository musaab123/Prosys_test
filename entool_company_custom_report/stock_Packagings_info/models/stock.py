from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, float_round
import logging

_logger = logging.getLogger(__name__)




 
class CustomStockMove(models.Model):
    _inherit = 'stock.move'

    
    # product_uom_qty_demand = fields.Float(
    #     string='Demand', compute='_compute_product_uom_qty_demand', store=True)  
    product_uom_qty = fields.Float(string='Demand', compute='_compute_product_uom_qty_demand', store=True ,default=1.0,)
    
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
    
    quantity_done = fields.Float(
        'Quantity Done', compute='_quantity_done_compute_test', digits='Product Unit of Measure',
        inverse='_quantity_done_set', store=True)
    
    @api.depends('product_id', 'product_packaging_qty', 'product_packaging_id', 'product_uom')
    def _compute_product_uom_qty_demand(self):
        for line in self:
            if not line.product_packaging_id:
                line.product_uom_qty = 0.0
                continue

            packaging_uom = line.product_packaging_id.product_uom_id
            qty_per_packaging = line.product_packaging_id.qty
            product_uom_qty = packaging_uom._compute_quantity(
                line.product_packaging_qty * qty_per_packaging, line.product_uom)

            if float_compare(product_uom_qty, line.product_uom_qty, precision_rounding=line.product_uom.rounding) != 0:
                line.product_uom_qty = product_uom_qty
    

  

    

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
                


    @api.depends('product_packaging_id', 'product_uom', 'done_qty_package')
    def _quantity_done_compute_test(self):
        for line in self:
            if not line.product_packaging_id:
                line.quantity_done = False
            else:
                packaging_uom = line.product_packaging_id.product_uom_id
                packaging_uom_qty = line.product_uom._compute_quantity(line.done_qty_package, packaging_uom)
                line.quantity_done = float_round(
                    packaging_uom_qty * line.product_packaging_id.qty,
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







   
