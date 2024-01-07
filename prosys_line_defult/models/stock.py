from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    allow_count_with_uom = fields.Boolean(compute='check_if_allow_uom')

    def check_if_allow_uom(self):
        check_val = self.user_has_groups('prosys_line_defult.group_count_with_uom')
        if check_val:
            for rec in self:
                rec.allow_count_with_uom = True
        else:
            for rec in self:
                rec.allow_count_with_uom = False

    @api.onchange('allow_count_with_uom')
    def onchange_allow_count_with_uom(self):
        check_val = self.user_has_groups('prosys_line_defult.group_count_with_uom')
        if check_val:
            for rec in self:
                rec.allow_count_with_uom = True
        else:
            for rec in self:
                rec.allow_count_with_uom = False


class StockMove(models.Model):
    _inherit = "stock.move"

    product_packaging_quantity = fields.Float(compute='set_product_packaging_quantity', string='Package Demand')
    product_packaging_qty_done = fields.Float(string='Package Done')

    @api.onchange('quantity_done')
    def set_product_packaging_qty_done(self):
        for rec in self:
            if rec.product_packaging_id:
                if rec.quantity_done:
                    rec.product_packaging_qty_done =  rec.quantity_done / rec.product_packaging_id.qty
                else:
                    rec.product_packaging_qty_done = 0

    @api.onchange('product_packaging_qty_done')
    def set_quantity_done(self):
        for rec in self:
            if rec.product_packaging_id:
                if rec.product_packaging_qty_done:
                    rec.quantity_done = rec.product_packaging_qty_done * rec.product_packaging_id.qty


    def set_product_packaging_quantity(self):
        for rec in self:
            if rec.product_packaging_id:
                rec.product_packaging_quantity =  rec.product_uom_qty / rec.product_packaging_id.qty
            else:
                rec.product_packaging_quantity = 0
