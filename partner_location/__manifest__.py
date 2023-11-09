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
    'depends': ['base','base_geolocalize', 'account','crm_enterprise','crm','web_map','industry_fsm','project'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/customer_location_view.xml',
        'views/project_task_inherit.xml',
        'views/google_map_view.xml',
        'views/sale_lines_view.xml',
        # 'views/add_task_wizard.xml',
        'views/edit_project_task.xml',




        


        

    ],
    'assets': {
        'web.assets_backend': [
            'partner_location/static/src/js/custom_inherit.js',

        ],
     
       
    },
    'images': ['static/description/location.png'],

    'installable': True,
    'application': False,
}

