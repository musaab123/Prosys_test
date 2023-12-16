from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = "product.category"

    total_route_ids = fields.Many2many(
        'stock.location.route',
        'product_category_route_rel',
        'category_id',
        'route_id',
        string='Total Routes',
        domain="[('company_id', '=', False), '|', ('company_id', '=', company_id), ('company_id', '=', False)]"
    )

    route_ids = fields.Many2many(
        'stock.location.route',
        'product_category_route_rel',
        'category_id',
        'route_id',
        string='Routes',
        domain="[('company_id', '=', False), '|', ('company_id', '=', company_id), ('company_id', '=', False)]"
    )

class ProductTemplate(models.Model):
    _inherit = ['product.template']

    company_id = fields.Many2one('res.company', string='Company', invisible=True, index=True, default=lambda self: self.env.company)
