# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


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

    shipping_company = fields.Char("Shipping Company")
    customer_address = fields.Char("Customer Address")
    shipping_document_number = fields.Char("Shipping document number")
    shipping_date = fields.Date("Shipping Date")
    number_of_packages = fields.Char("Number Packages")
    amount_shipment = fields.Char("Total Amount Shipment")
    payment_term = fields.Char("Payment Term")
    container_ids = fields.One2many('container.details','sale_id',string="Containers")


     


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['shipping_type'] = self.shipping_type
        invoice_vals['shipping_company'] = self.shipping_company
        invoice_vals['customer_address'] = self.customer_address
        invoice_vals['shipping_document_number'] = self.shipping_document_number
        invoice_vals['shipping_date'] = self.shipping_date
        invoice_vals['number_of_packages'] = self.number_of_packages
        invoice_vals['amount_shipment'] = self.amount_shipment
        invoice_vals['payment_term'] = self.payment_term
        invoice_vals['container_ids'] = [(6,0,self.container_ids.ids)]
        return invoice_vals




class Containers(models.Model):
    _name = 'container.details'

    sale_id = fields.Many2one('sale.order','Sale Order')
    purchase_id = fields.Many2one('purchase.order','Purchase Order')
    account_id = fields.Many2one('account.move','Accounts')
    
    shipment_arrival_date = fields.Date("Shipment Arrival Date")
    shipping_port = fields.Char("Shipping Port")
    Port_arrival= fields.Char("Arrival Port")
    container_type= fields.Char("Container Type")



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_id = fields.Many2one('account.move','Invoice Number')
    container_ids = fields.One2many('container.details','sale_id',string="Containers" , compute="_get_questions")


    def _get_questions(self):
            self.container_ids = self.env['container.details'].search([])




