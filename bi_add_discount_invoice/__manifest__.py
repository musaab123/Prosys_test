# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Discount on Invoice Analysis Report',
    'version': '16.0.0.1',
    'category': 'Accounting',
    'license': 'OPL-1',
    'summary': 'Invoice Analysis Discount Odoo App helps user to add discount filter on invoice analysis. User can easily enable/disable discount filter on invoice analysis. User can show discount in percentage on invoice analysis.',
    'description': """

            Add Discount Invoice in odoo,
            Invoice Analysis Discount in odoo,
            Discount on invoice analysis in odoo,
            Enable/Disable Discount on Invoice Analysis in odoo,
            Discount Filter in odoo,
            Discount in percentage in odoo,

sale_tree_view_inherit.xml
    """,
    'author': 'Prosys',
    'website': 'https://www.Prosys.com',
    'depends': ['account','sale','bi_sale_purchase_discount_with_tax'],

    "data": [
        'views/sale_tree_view_inherit.xml',
        'views/account_tree_view_inherit.xml'

    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/Z_WBvRHMq1A',
    "images":['static/description/Banner.gif'],
}
