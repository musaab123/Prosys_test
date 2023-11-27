from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the PO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += (
                                           line.product_qty * line.price_unit * line.discount) / 100
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_discount': amount_discount,
                'amount_total': amount_untaxed + amount_tax,
            })

    discount_type = fields.Selection(
        [('percent', 'Percentage'), ('amount', 'Amount')],
        string='Discount type',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default='percent')
    discount_rate = fields.Float('Discount Rate',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'sent': [('readonly', False)]})
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True,
                                     readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True,
                                 compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True,
                                   compute='_amount_all',
                                   track_visibility='always')
    amount_discount = fields.Monetary(string='Discount', store=True,
                                      readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'),
                                      track_visibility='always')
    
    amount_untaxed_sale = fields.Monetary(string="Untaxed Amount Before Discount", store=True, compute='_compute_untaxed_amounts', tracking=5)

    
    @api.depends('order_line')
    def _compute_untaxed_amounts(self):
        """Compute the total amounts of the Price Unit."""
        total =0
        for line in self.order_line:
            if line.taxes_id:
                if line.taxes_id.price_include:
                    total+= (line.price_unit* line.product_qty)/1.15
                    # total = total/1.15
                else:
                    total+= (line.price_unit* line.product_qty)

            else:
                total+= (line.price_unit* line.product_qty)
        
        self.amount_untaxed_sale = total
        
    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        for order in self:
            if order.discount_type == 'percent':
                print(" prisent --------------------->")
                for line in order.order_line:
                    line.discount = order.discount_rate
                    print("discount ---------------------->", line.discount)

            else:
                total = discount = 0.0
                for line in order.order_line:
                    total += round((line.product_qty * line.price_unit))
                if order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = order.discount_rate
                for line in order.order_line:
                    line.discount = discount
                    # print(line.discount)
                    new_sub_price = (line.price_unit * (discount / 100))
                    print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",new_sub_price)
                    line.total_discount = line.price_unit - new_sub_price


    def _prepare_invoice(self, ):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
            'amount_discount': self.amount_discount,
            'amount_untaxed_sale': self.amount_untaxed_sale,


        })
        return invoice_vals

    def button_dummy(self):

        self.supply_rate()
        return True



class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_account_move_line(self, move=False):
        invoice_vals = super(PurchaseOrderLine, self)._prepare_account_move_line()
        invoice_vals.update({
            'discount': self.order_id.amount_discount,
    
        })
        return invoice_vals
    
    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
           
            product=self.product_id,
            taxes=self.taxes_id,
            price_unit=self.price_unit,
            quantity=self.product_uom_qty,
            discount=self.discount,
            price_subtotal=self.price_subtotal,
        )


    @api.depends('product_qty', 'discount', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })




    discount = fields.Float(string='Discount (%)', default=0.0)
    total_discount = fields.Float(string="Total Discount", default=0.0, store=True)
    


   



            
  