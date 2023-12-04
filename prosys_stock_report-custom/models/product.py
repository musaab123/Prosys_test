from odoo import models, fields, api
    

class ProductProduct(models.Model):
    _inherit = "product.product"

    expected_profit = fields.Float(string='Expected profit', compute="calculate_expected_profit")   
    packag_info = fields.Float(string="Packaging Qty", related='packaging_ids.qty')



    @api.depends('lst_price','qty_available')
    def calculate_expected_profit(self):
        for rec in self:
            rec.expected_profit = rec.lst_price * rec.qty_available

  



