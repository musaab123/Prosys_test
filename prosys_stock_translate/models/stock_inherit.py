from odoo import models, fields, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    name = fields.Char(translate=True)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    name = fields.Char(translate=True)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    name = fields.Char(string='Category Name', translate=True)





    # parent_id = fields.Many2one(translate=True)



