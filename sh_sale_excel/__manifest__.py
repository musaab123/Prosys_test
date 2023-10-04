# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sales Excel Reports | Sales Order Excel Reports | Quotation Excel Reports | Sale Excel Report | Sale Orders Excel Report ",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "license": "OPL-1",
    "category": "Sales",
    "summary": "Merge Excel Report Of Sales Order, Combine Sale Order Excel Report, Mass Excel Report, Bulk Sale Excel Report,Quotation Excel,Excel Report Of Quotation,Print Sale Excel Report,Print Sale Order Excel Report,Download Sale Excel Report Odoo", 
    "description":  """If you want to get excel reports of sales order/quotation. So here we build a module that can help to print the excel report of the sales order/quotation. You can get an excel report separate sheet of each order also. Cheers!""",
    "depends": [
        'sale_management','stock','sale'
    ],
    "data": [
        
        "data/excel_report_server_report.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["static/description/background.png"],
    "price": "15",
    "currency": "EUR"
}
