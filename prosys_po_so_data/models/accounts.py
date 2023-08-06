# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_show_field = fields.Boolean('is show Account Purchase Deteles')
    sale_show_field = fields.Boolean('is show Account Sale Deteles')


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

    shipping_type = fields.Selection(
        selection=[
            ('by_air', 'By Air'),
            ('overland', 'Overland'),
            ('by_sea', 'By Sea'),
           
        ],
        string='Shipping Type',
        index=True,
    )
    shipping_document_type = fields.Char("Shipping document Type")
    shipping_company = fields.Char("Shipping Company")
    exw  = fields.Char("EXW")
    shipping_document_number = fields.Char("Shipping document number")
    shipping_date = fields.Date("Shipping Date")
    number_of_packages = fields.Char("Number Packages")
    amount_shipment = fields.Char("Total Amount Shipment")
    shipment_arrival_date = fields.Date("Shipment Arrival Date")
    shipping_port = fields.Char("Shipping Port")
    port_arrival= fields.Char("Arrival Port")
    container_type= fields.Char("Container Type")
    


     
    container_ids = fields.One2many('container.details','account_id',string="Containers")
    