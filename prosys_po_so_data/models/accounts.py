# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api


class AccountMove(models.Model):
    _inherit = 'account.move'

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
    shipping_document_type = fields.Char("Shipping document Type")
    shipping_company = fields.Char("Shipping Company")
    customer_address = fields.Char("Customer Address")
    fob_cif  = fields.Char(" FOB-CIF")
    shipping_document_number = fields.Char("Shipping document number")
    shipping_date = fields.Date("Shipping Date")
    number_of_packages = fields.Char("Number Packages")
    amount_shipment = fields.Char("Total Amount Shipment")
    payment_term = fields.Char("Payment Term")
    shipment_arrival_date = fields.Date("Shipment Arrival Date")
    shipping_port = fields.Char("Shipping Port")
    port_arrival= fields.Char("Arrival Port")
    container_type= fields.Char("Container Type")


     
    container_ids = fields.One2many('container.details','account_id',string="Containers")