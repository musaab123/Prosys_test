# -*- coding: utf-8 -*-


{
    'name': 'Partner Geolocation',
    'version': '16.0.1.0.0',
    'category': 'Contacts',
    'description': 'Partner Geolocation.',
    'summary': 'Partner Geolocation.',
    'author': 'musaab',
    'company': 'musaab',
    'maintainer': 'musaab ',
    'depends': ['base','base_geolocalize', 'account'],
    'data': [
        
        'views/customer_location_view.xml',


    ],
    'assets': {
        'web.assets_backend': [
            # 'partner_location/static/src/js/res_partner.js',
            # 'partner_location/static/src/js/res_partner_custom.js',
            'partner_location/static/src/js/custom_inherit.js',

           
        ],
       
    },
    'images': ['static/description/location.png'],

    'installable': True,
    'application': False,
}

