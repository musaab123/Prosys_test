{
    'name': 'Product Barcode Sequence',
    'version': '16.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Product Barcode Sequence',
    'author': 'prosys',
    'company': 'prosys',
    'maintainer': 'prosys',
    'images': ['static/description/banner.png'],
    'depends': ['product','stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/barcode.xml',
        'views/barcode.xml',
        
    ],
    
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
