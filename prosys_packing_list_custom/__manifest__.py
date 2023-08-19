# -*- coding: utf-8 -*-
##############################################################################
#
#    NCTR, Nile Center for Technology Research
#    Copyright (C) 2021-2022 NCTR (<http://www.nctr.sd>).
#
##############################################################################
{
    "name": "Design reports for sales, purchases and accounts",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "NCTR",
    "website": "http://www.nctr.sd",
    "depends":['sale','account','stock','prosys_po_so_data','product_barcode_sequence','product_hs_code_inventory','product_factory_inventory','product_brand_inventory'],
    "data": [
        'security/group_company_employee.xml',
        'reports/modren_invoice_template.xml',
        'reports/delevry_slip_custom.xml',

        'reports/report.xml',
    ],
    "installable": True,
    "active": True,
}

