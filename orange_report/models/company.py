from odoo import api,fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = 'sequence, id'


    product_packaging_id = fields.Many2one(
        comodel_name='product.packaging',
        string="Packaging",
        store=True, readonly=False, precompute=True,
        domain="[('sales', '=', True), ('product_id','=',product_id)]",
        check_company=True)
    
    product_packaging_qty = fields.Float(
        string="Packaging Quantity",
        store=True, readonly=False, precompute=True)
    
    sequence = fields.Integer(string="Sequence", default=10)

    
    def _prepare_invoice_line(self,**optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res['sequence'] = self.sequence
        res['product_packaging_id'] = self.product_packaging_id.id 
        res['product_packaging_qty'] = self.product_packaging_qty
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    def action_confirm(self):
        res = super(PurchaseOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                picking = self.env['purchase.order.line'].search([
                    ('purchase_id', '=', order.id),
                  
                ], limit=1)
                if picking:
                    picking.product_packaging_qty = line.product_packaging_qty
        return res

   

 





