# -*- coding: utf-8 -*-


from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

   
    amount_shipment = fields.Char("Total Amount Shipment")
    shipping_document_number = fields.Char("Shipping document Number")
    shipping_document_type = fields.Char("Shipping document Type")
    shipping_date = fields.Date("Shipping Date")
    number_of_packages = fields.Char("Number Packages")
    shipping_company = fields.Char("Shipping Company")
    exw  = fields.Char("EXW")
    shipping_type = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        index=True,
    )
    container_ids = fields.One2many('container.details','purchase_id',string="Containers")
    package_ids = fields.One2many('packing.list','purchase_id',string="Packages")



    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals['shipping_document_number'] = self.shipping_document_number
        invoice_vals['shipping_document_type'] = self.shipping_document_type
        invoice_vals['amount_shipment'] = self.amount_shipment


        invoice_vals['shipping_date'] = self.shipping_date
        invoice_vals['number_of_packages'] = self.number_of_packages
        invoice_vals['shipping_company'] = self.shipping_company
        invoice_vals['exw'] = self.exw
        invoice_vals['shipping_type'] = self.shipping_type

        invoice_vals['container_ids'] = [(6,0,self.container_ids.ids)]
        invoice_vals['package_ids'] = [(6,0,self.package_ids.ids)]

        return invoice_vals





