from odoo import api,fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move.line'


    product_packaging_id = fields.Many2one(
            comodel_name='product.packaging',
            string="Packaging",
            store=True, readonly=False, precompute=True,
            domain="[('sales', '=', True), ('product_id','=',product_id)]",
            check_company=True)
    
    product_packaging_qty = fields.Float(
            string="Packaging Quantity",
            store=True, readonly=False, precompute=True)



class StockMove(models.Model):
    _inherit = 'stock.move'


    product_packaging_id = fields.Many2one(
            comodel_name='product.packaging',
            string="Packaging",
            store=True, readonly=False, precompute=True,
            domain="[('sales', '=', True), ('product_id','=',product_id)]",
            check_company=True)
    
    product_packaging_qty = fields.Float(
            string="Packaging Quantity",
            store=True, readonly=False, precompute=True)
