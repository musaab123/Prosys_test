{
    'name': 'Factories in Inventory',
    'version': '16.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Factories in Inventory',
    'author': 'prosys',
    'company': 'prosys',
    'maintainer': 'prosys',
    'images': ['static/description/banner.png'],
    'depends': ['stock','sale_management','purchase','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/factory.xml',
        'views/factory_sale_views.xml',
        'views/sale_report_views.xml',
        'views/factory_purchase_views.xml',
        'views/purchase_report_views.xml',
        'views/account_invoice_report_view.xml',
        'views/factory_invoice_views.xml'
        
    ],
    
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
