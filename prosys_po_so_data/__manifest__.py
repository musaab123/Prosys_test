# -*- coding: utf-8 -*-


{
    'name': 'Prosys Data of Stock,SO and PO',
    'version': '16.0.1.0.0',
    'category': 'Contacts',
    'description': 'Adding new information fields in partners,sales,purchase and accounts.',
    'summary': 'Adding new information fields in partners,sales,purchase and accounts.',
    'author': 'PROSYS',
    'company': 'PROSYS',
    'maintainer': 'Prosys ',
    'depends': ['base', 'sale','sale_stock','purchase_stock','sale_purchase','purchase', 'account' ,'stock' ,'hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_purchase_group.xml',

        'views/sales_view.xml',
        'views/purchase_view.xml',
        'views/accounts_view.xml',
        # 'views/partner_view.xml',
        'views/stock_view.xml',

    ],
    'installable': True,
    'application': False,
}

