# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    shipping_type_id = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        index=True,
    )

    shipping_company_id = fields.Char("Shipping Company")
    shipping_document_number_id = fields.Char("Shipping document number")
    shipping_date_id = fields.Date("Shipping Date")
    number_of_packages_id = fields.Char("Number Packages")
    amount_shipment_id = fields.Char("Total Amount Shipment")
    shipping_document_type_id = fields.Char("Shipping document Type")
    exw_id  = fields.Char("EXW")


    container_ids = fields.One2many('container.details','sale_id',string="Containers")


     


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['shipping_type_id'] = self.shipping_type_id
        invoice_vals['shipping_company_id'] = self.shipping_company_id
        invoice_vals['shipping_document_number_id'] = self.shipping_document_number_id
        invoice_vals['shipping_date_id'] = self.shipping_date_id
        invoice_vals['number_of_packages_id'] = self.number_of_packages_id
        invoice_vals['amount_shipment_id'] = self.amount_shipment_id
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

    current_user = fields.Boolean('is show Stock Purchase')
    sale_show = fields.Boolean('is show Stock Sale')

    amount_shipment_id = fields.Char("Total Amount Shipment" ,related='sale_id.amount_shipment_id',store=True)
    amount_shipment = fields.Char("Total Amount Shipment" ,related='purchase_id.amount_shipment',store=True)

    
    shipping_document_number_id = fields.Char("Shipping document Number",related='sale_id.shipping_document_number_id',store=True)
    shipping_document_number = fields.Char("Shipping document Number",related='purchase_id.shipping_document_number',store=True)

    shipping_document_type_id = fields.Char("Shipping document Type" ,related='sale_id.shipping_document_type_id',store=True)
    shipping_document_type = fields.Char("Shipping document Type" ,related='purchase_id.shipping_document_type',store=True)

    shipping_date_id = fields.Date("Shipping Date" ,related='sale_id.shipping_date_id',store=True)
    shipping_date = fields.Date("Shipping Date" ,related='purchase_id.shipping_date',store=True)


    number_of_packages_id = fields.Char("Number Packages" ,related='sale_id.number_of_packages_id',store=True)
    number_of_packages = fields.Char("Number Packages" ,related='purchase_id.number_of_packages',store=True)

    shipping_company_id = fields.Char("Shipping Company" ,related='sale_id.shipping_company_id',store=True)
    shipping_company = fields.Char("Shipping Company" ,related='purchase_id.shipping_company',store=True)

    exw_id  = fields.Char("EXW" ,related='sale_id.exw_id',store=True)
    exw  = fields.Char("EXW" ,related='purchase_id.exw',store=True)

    shipping_type_id = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        index=True,
        store=True,
        related='sale_id.shipping_type_id'
    )

    shipping_type = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        index=True,
        store=True,
        related='purchase_id.shipping_type'
    )



    # def _default_sale_order_amount(self):
    #     sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
    #     return sale_order.amount_shipment

    # sale_order_amount = fields.Char(default=_default_sale_order_amount, string='Amount', readonly=True)


    invoice_id = fields.Many2one('account.move','Invoice Number')
    container_ids = fields.One2many('container.details','sale_id',string="Containers" , compute="_get_questions")


    def _get_questions(self):
        for rec in self:
            if rec.sale_id:
                rec.container_ids = self.env['container.details'].search([('sale_id','=',rec.sale_id.id)])
            if rec.purchase_id:
                rec.container_ids = self.env['container.details'].search([('purchase_id','=',rec.purchase_id.id)])




    




