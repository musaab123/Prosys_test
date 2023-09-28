# -*- coding: utf-8 -*-


{
    'name': 'Customer Sale Location',
    'version': '16.0.1.0.0',
    'category': 'Contacts',
    'description': 'Customer Sale Location.',
    'summary': 'Customer Sale Location.',
    'author': 'musaab',
    'company': 'musaab',
    'maintainer': 'musaab ',
    'depends': ['base','sale', 'account'],
    'data': [
        
        'security/location_permition.xml',
        'views/customer_location_view.xml',
        'views/account_customer_location.xml',



        
       

    ],
    'assets': {
        'web.assets_backend': [
            'customer_location_custom/static/src/js/my_attendances.js',
           
        ],
        'web.assets_frontend': [
            'customer_location_custom/static/src/js/sale_order_geolocation.js',
        ],
 

    },
    'images': ['static/description/location.png'],

    'installable': True,
    'application': False,
}

