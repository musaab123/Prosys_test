# -*- coding: utf-8 -*-
{
    'name': "posys partner extra info",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Manages the Discount in Sale  , Purchase Order and in whole Sale order/Purchase order basis on Fix
        and Percentage wise as well as calculate

        This module also have following separated features.
            -List Price Discount on Invoice, List Price on purchase order, List Price Discount on Sales order
            -Discount on sale order line, Discount on purchase order line, Discount on Invoice line
            -Discount purchase, Discount sale,Discount Invoice, Discount POS, Disount Order,Order Discount, Point of Sale Discount,Discont on pricelist, Fixed Discount, Percentage Discount, Commission, Discount Tax.
            -All in One Discount, All discount, Sales Discount, Purchase Discount,Sales Invoice Discount, Purchase Invoice Discount,Odoo Discount, OpenERP Discount, Sale Order Discount, Purchase order discount, Invoice line Discount,Discount with Taxes, Order line Discount, sale line discount, purchase line discount,Discount on line.Discount Feature, Discount for all

    """,

    'author': "Prosys",
    'website': "https://www.yourcompany.com",

   
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account','stock','sale','contacts','hr','purchase','base_geolocalize'],



    'data': [
        'security/ir.model.access.csv',
        'views/partner_activty.xml',
        'views/made_in_views.xml',
        'views/sales_view.xml',
        'views/jop_postion.xml',
        "report/sale_report_view.xml",



        
    ],
    'assets': {
        'web.assets_backend': [
            'posys_partner_extra_info/static/src/js/custom_inherit_wiz.js',

           
        ],
       
    },

}
