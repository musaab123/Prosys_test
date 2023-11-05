from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_name = fields.Char(string='Vendor Product Name')
    product_code = fields.Char(string='Vendor Product Code')

class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_name = fields.Char(string='Vendor Product Name', related='purchase_order_id.order_line.product_name', store=True)
    product_code = fields.Char(string='Vendor Product Code', related='purchase_order_id.order_line.product_code', store=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_name = fields.Char(string='Vendor Product Name', related='purchase_id.order_line.product_name', store=True)
    product_code = fields.Char(string='Vendor Product Code', related='purchase_id.order_line.product_code', store=True)

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_name = fields.Char(string='Vendor Product Name', related='purchase_line_id.product_name', store=True)
    product_code = fields.Char(string='Vendor Product Code', related='purchase_line_id.product_code', store=True)



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_name = fields.Char(string='Vendor Product Name')
    product_code = fields.Char(string='Vendor Product Code')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        ret = super(PurchaseOrder, self).button_confirm()

        for order_line in self.order_line:
            product_tmpl_id = self.env["product.product"].search([("id","=", order_line.product_id.id )]).product_tmpl_id
            supplier_info = self.env["product.supplierinfo"].search([("product_tmpl_id","=",product_tmpl_id.id),("partner_id","=",self.partner_id.id)],limit=1)
            supplier_info.product_name = order_line.product_name
            supplier_info.product_code = order_line.product_code
            
        return ret           
                


    product_name = fields.Char(string='Vendor Product Name')
    product_code = fields.Char(string='Vendor Product Code')

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_template_id = fields.Many2one(
        'product.template',
        related='product_id.product_tmpl_id',
        string='Product Template',
        store=True,
        readonly=True,
    )

    @api.onchange('product_template_id', 'partner_id')
    def _onchange_product_template_id(self):
        if self.product_template_id and self.partner_id:
            self.product_name = self.product_name
            self.product_code = self.product_code

class ProductProduct(models.Model):
    _inherit = 'product.template'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            purchase_order_lines = self.purchase_order_ids.order_line.filtered(
                lambda line: line.order_id.partner_id == self.partner_id
            )

            if purchase_order_lines:
                purchase_order_line = purchase_order_lines[0]
                self.product_name = purchase_order_line.product_name
                self.product_code = purchase_order_line.product_code


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'


    product_name = fields.Char(string='Vendor Product Name')
    product_code = fields.Char(string='Vendor Product Code')

   









# class ProductSupplierInfo(models.Model):
#     _inherit = 'product.supplierinfo'

#     product_name = fields.Char(string='Vendor Product Name')
#     product_code = fields.Char(string='Vendor Product Code')

    



