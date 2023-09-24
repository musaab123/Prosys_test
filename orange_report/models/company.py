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
    _order = 'sequence, id'

    product_packaging_id = fields.Many2one('product.packaging', string='Packaging', domain="[('purchase', '=', True), ('product_id', '=', product_id)]", check_company=True,
                                            store=True, readonly=False)
    product_packaging_qty = fields.Float('Packaging Quantity', store=True, readonly=False)
    sequence = fields.Integer(string='Sequence', default=10)
    

    def _prepare_invoice_line(self,**optional_values):
        res = super(PurchaseOrder, self)._prepare_invoice_line(**optional_values)
        res['sequence'] = self.sequence
        res['product_packaging_id'] = self.product_packaging_id.id 
        res['product_packaging_qty'] = self.product_packaging_qty
        return res

   
   

 





