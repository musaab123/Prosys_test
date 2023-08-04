# -*- coding: utf-8 -*-


from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # def _get_employee_related(self):
    #     employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
    #     if employee:
    #         return employee.id
    #     else:
    #         return False

    # part_id = fields.Char('Partner ID',related='partner_id.partner_id',store=True)
    # vendor_bill_number = fields.Char('Vendor Bill Number')
    # responsible_employee = fields.Many2one('hr.employee','Responsible Employee',default=_get_employee_related)
    amount_shipment = fields.Char("Total Amount Shipment")
    customer_address = fields.Char("Customer Address")

    shipping_document_number = fields.Char("Shipping document Number")
    shipping_document_type = fields.Char("Shipping document Type")
    shipping_date = fields.Date("Shipping Date")
    payment_term = fields.Char("Payment Term")
    number_of_packages = fields.Char("Number Packages")
    shipping_company = fields.Char("Shipping Company")
    fob_cif  = fields.Char(" FOB-CIF")
    shipping_type = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        required=True,
        index=True,
    )
    container_ids = fields.One2many('container.details','purchase_id',string="Containers")


    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals['shipping_document_number'] = self.shipping_document_number
        invoice_vals['shipping_document_type'] = self.shipping_document_type
        invoice_vals['amount_shipment'] = self.amount_shipment
        invoice_vals['customer_address'] = self.customer_address


        invoice_vals['shipping_date'] = self.shipping_date
        invoice_vals['payment_term'] = self.payment_term
        invoice_vals['number_of_packages'] = self.number_of_packages
        invoice_vals['shipping_company'] = self.shipping_company
        invoice_vals['fob_cif'] = self.fob_cif
        invoice_vals['shipping_type'] = self.shipping_type

        invoice_vals['container_ids'] = [(6,0,self.container_ids.ids)]
        return invoice_vals

