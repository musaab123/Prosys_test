from odoo import models, fields, api
from odoo.exceptions import UserError

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    can_sale = fields.Boolean('Sale')

    @api.onchange('order_line')
    def check_margin(self):
        for line in self.order_line:
            if self.can_sale:
                # Check if cost price is higher than sale price
                 if line.price_unit > line.product_id.standard_price:
                   raise UserError("Sale price is low than cost price")
            else:
                # Check if sale price is lower than cost price
               
                if line.price_unit < line.product_id.standard_price:
                    raise UserError("Sale price is low than cost price")
    

