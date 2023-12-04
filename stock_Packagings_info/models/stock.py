from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, float_round
import logging

_logger = logging.getLogger(__name__)


class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'

    total_demand = fields.Float(
        string="Total Demand",
        compute='_compute_total_demand',
        store=True, readonly=True, )
    total_packaging_qty = fields.Float(
        string="Total per carton",
        compute='_compute_packaging_qty',
        store=True, readonly=True, )
    
    @api.depends('move_ids_without_package')
    def _compute_total_demand(self):
        total = 0
        for line in self.move_ids_without_package:
            print("line ---------------------------->",line)
            total += line.product_uom_qty
        self.total_demand = total


    @api.depends('move_ids_without_package')
    def _compute_packaging_qty(self):
        total = 0
        for line in self.move_ids_without_package:
            print("line ---------------------------->",line)
            total += line.product_packaging_qty
        self.total_packaging_qty = total



    



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
    
    # total_demand = fields.Float(
    #     string="Total Demand",
    #     store=True, readonly=True, )
    

    

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
