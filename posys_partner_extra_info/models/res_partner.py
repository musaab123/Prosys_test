from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
class ResPArtnerInherit(models.Model):
    _inherit = 'res.partner'

    categ_id = fields.Many2many('clint.activty', string='Clint Activty')
    trade_name = fields.Char(string="Trade Name")
    cr = fields.Char(string="Commercial Register")
    # vat = fields.Char(required=True)
    mobile = fields.Char(required=True)


    @api.model
    def search_by_trade_name(self, trade_name):
        partners = self.search([('trade_name', 'ilike', trade_name)])
        return partners
    
    @api.model
    def search_by_trade_name(self, cr):
        partners = self.search([('cr', 'ilike', cr)])
        return partners



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    quantity_on_hand = fields.Float(string='Quantity On Hand', compute='_compute_quantity_on_hand')

    @api.depends('product_id', 'product_id.product_variant_ids', 'product_uom_qty')
    def _compute_quantity_on_hand(self):
        for line in self:
            if line.product_id:
                quantity_on_hand = 0.0
                for variant in line.product_id.product_variant_ids:
                    # Assuming that your product variant has a field named 'qty_available'
                    quantity_on_hand += variant.qty_available * line.product_uom_qty
                line.quantity_on_hand = quantity_on_hand
            else:
                line.quantity_on_hand = 0.0


    def _prepare_invoice_line(self, **optional_values):
        """Prepare the values to create the new invoice line for a sales order line.

        :param optional_values: any parameter that should be added to the returned invoice line
        :rtype: dict
        """
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({
            'quantity_on_hand': self.quantity_on_hand,
        })
        return res
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # sale_order_count = fields.Integer(related='partner_id.sale_order_count', store=True)

    driver_id = fields.Many2one('hr.employee', string="Driver", help='Select corresponding Employee')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['driver_id'] = self.driver_id.id       
        return invoice_vals
    
    sale_order_count = fields.Integer(related='partner_id.sale_order_count', store=True)
    is_first_sale_order = fields.Boolean(default=False, copy=False)

    @api.model
    def create(self, values):
        order = super(SaleOrder, self).create(values)
        if order.partner_id and order.partner_id.sale_order_count == 1:
            order.is_first_sale_order = True
        return order
    
    # has_sale_order = fields.Boolean(compute="first_sale_order")
    
    # @api.depends("partner_id")
    # def first_sale_order(self):
    #     for rec in self:
    #         if rec.partner_id.sale_order_count >0:
    #             rec.has_sale_order=True
    #         else:
    #             rec.has_sale_order=False

        
    # @api.depends("partner_id")
    # def first_sale_order(self):
   
    #     # Check if it's the customer's first sale order
    #     if order.partner_id and order.partner_id.sale_order_count == 0:
    #         warning_message = _("Welcome! This is your first sale order.")

    #         # Display a warning message
    #         if warning_message:
    #             return {'warning': {'title': _('Warning!'), 'message': warning_message}}

    #     return order


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order','Sale Order')

   
    driver_id = fields.Many2one(related='sale_id.driver_id', readonly=False, store=True)


class AccountMove(models.Model):
    _inherit = 'account.move'
    # driver_id = fields.Char(string="Driver" ,store=True)
    driver_id = fields.Many2one('hr.employee', string="Driver", help='Select corresponding Employee')

class AccountMove(models.Model):
    _inherit = 'account.move.line'
    quantity_on_hand = fields.Float(string='Quantity On Hand')



class res_partner(models.Model):
    _inherit = 'res.partner'

    additional_code =fields.Char("Additional Code")
    buliding_number =fields.Char("Bulding Number")
    region_id = fields.Many2one('regional.area', string='Regional Area',required=True)
    district_id = fields.Many2one('district.district', string='District')


    google_map_link = fields.Char(string='Google Map Link')

    sale_order_count = fields.Integer(compute='_compute_sale_order_count', store=True)

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for partner in self:
            partner.sale_order_count = len(partner.sale_order_ids)











