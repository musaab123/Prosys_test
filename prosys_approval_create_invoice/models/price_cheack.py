from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def check_margin(self):
        for line in self.order_line:
            if line.price_unit < line.product_id.standard_price:
                raise UserError("sale price is lower than cost price")
            
    
    

