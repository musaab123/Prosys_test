{
    'name': 'Stock Picking  Workflow',
    'version': '0.0.1',
    'summary': 'Stock Picking  Workflow',
    'description': 'Stock Picking  Workflow',
    'category': 'Category',
    'author': 'Prosys',
    'website': 'Website',
    'license': 'LGPL-3',
    'depends': ['sale', 'purchase','stock'],
    'data': [
        'security/security.xml',
        'views/sale_order_workflow_view.xml',
        # 'views/po_order_workflow_view.xml',
    ],
    'demo': ['Demo'],
    'installable': True,
    'auto_install': False
}
