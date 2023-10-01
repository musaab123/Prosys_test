from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

from odoo import api, fields, models, _

class SaleConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    restrect_sale = fields.Boolean(string='Restrict Product Sale Without Stock')
    restrict_sale_user_ids = fields.Many2many('res.partner', string='Available User')

    def set_values(self):
        super(SaleConfiguration, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('prosys_restrict_out_of_stock.restrect_sale', self.restrect_sale)
        self.env['ir.config_parameter'].sudo().set_param('prosys_restrict_out_of_stock.restrict_sale_user_ids', ','.join(map(str, self.restrict_sale_user_ids.ids)))

    def get_values(self):
        res = super(SaleConfiguration, self).get_values()
        restrect_sale = self.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrect_sale', default=False)
        restrict_sale_user_ids = self.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrict_sale_user_ids', default='').split(',')
        # Filter out empty strings and convert to integers
        restrict_sale_user_ids = [int(user_id) for user_id in restrict_sale_user_ids if user_id]
        res.update(
            restrect_sale=bool(restrect_sale),
            restrict_sale_user_ids=[(6, 0, restrict_sale_user_ids)],
        )
        return res





class ProductTemplate(models.Model):
    _inherit = "product.template"

    unavailable_qty = fields.Boolean(string='Sell Unavailable Qty')
    qty_available = fields.Float(string='Available Quantity', compute='_compute_qty_available')

    @api.depends('product_variant_ids', 'product_variant_ids.qty_available')
    def _compute_qty_available(self):
        for template in self:
            template.qty_available = sum(template.product_variant_ids.mapped('qty_available'))

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.onchange('order_line')
    def check_margin(self):
        for order in self:
            restrect_sale = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrect_sale', default=False)
            restrict_sale_user_ids = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrict_sale_user_ids', default='')

            restrict_sale_user_ids = [int(user_id) for user_id in restrict_sale_user_ids.split(',') if user_id]

            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", restrict_sale_user_ids)

            for line in order.order_line:
                if line.product_template_id.unavailable_qty and restrect_sale:
                    if order.partner_id.id not in restrict_sale_user_ids:
                        if line.product_uom_qty > line.product_template_id.qty_available:
                           raise ValidationError(_("You can't confirm this order because of the following reasons:\n"
                       "You added ({}) of ({}) but you only have ({}) available in YourCompany Warehouse.\n"
                       "To confirm this order, please contact the administrator.").format(line.product_uom_qty, line.product_template_id.name, line.product_template_id.qty_available))

                elif line.product_uom_qty > line.product_template_id.qty_available:
                            raise ValidationError(_("You can't confirm this order because of the following reasons:\n"
                       "You added ({}) of ({}) but you only have ({}) available in YourCompany Warehouse.\n"
                       "To confirm this order, please contact the administrator.").format(line.product_uom_qty, line.product_template_id.name, line.product_template_id.qty_available))




    # @api.onchange('order_line')
    # def check_margin(self):
    #     for order in self:
    #         restrect_sale = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrect_sale', default=False)
    #         restrict_sale_user_ids = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrict_sale_user_ids', default='').split(',')
    #         restrict_sale_user_ids = [int(user_id) for user_id in restrict_sale_user_ids if user_id]

    #         for line in order.order_line:
    #             if line.product_template_id.unavailable_qty and restrect_sale:
    #                 if line.product_uom_qty > line.product_template_id.qty_available:
    #                     if not (order.partner_id.id in restrict_sale_user_ids):
    #                         pass
    #             elif line.product_uom_qty > line.product_template_id.qty_available:
    #                 raise ValidationError(_("The required quantity is greater than the quantity in stock. Please check with the admin to grant permission or add it to the white list"))



    # @api.onchange('order_line')
    # def check_margin(self):
    #     for order in self:
    #         restrect_sale = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrect_sale', default=False)
    #         restrict_sale_user_ids = order.env['ir.config_parameter'].sudo().get_param('prosys_restrict_out_of_stock.restrict_sale_user_ids', default='').split(',')
    #         restrict_sale_user_ids = [int(user_id) for user_id in restrict_sale_user_ids if user_id]

    #         for line in order.order_line:
    #             if line.product_template_id.unavailable_qty and restrect_sale:
    #                 if line.product_uom_qty > line.product_template_id.qty_available:
    #                     if not any(partner.id in restrict_sale_user_ids for partner in order.partner_id):
    #                         pass
    #             elif line.product_uom_qty > line.product_template_id.qty_available:
    #                 raise ValidationError(_("The required quantity is greater than the quantity in stock. Please check with the admin to grant permission or add it to the white list"))

    @api.depends('partner_id')
    def _compute_restrect_sale(self):
        for order in self:
            order.restrect_sale = self.env['res.config.settings'].get_values().get('restrect_sale', False)

    @api.depends('partner_id')
    def _compute_restrict_sale_user_ids(self):
        for order in self:
            order.restrict_sale_user_ids = self.env['res.config.settings'].get_values().get('restrict_sale_user_ids', [])

    restrect_sale = fields.Boolean(
        string='Restrict Product Sale Without Stock',
        compute='_compute_restrect_sale',
        store=False
    )

    restrict_sale_user_ids = fields.Many2many(
        'res.partner',
        string='Available User',
        compute='_compute_restrict_sale_user_ids',
        store=False
    )
