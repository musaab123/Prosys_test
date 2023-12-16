# -*- coding: utf-8 -*-
{
    'name': "posys partner extra info",
    'summary': """
        This module enhances the functionality of 
        the res.partner model by introducing additional 
        fields and location features. It is designed to 
        provide more comprehensive information about partners in the system""",

    'description': """
        This module enhances the functionality of the 
        res.partner model by introducing additional fields 
        and location features. It is designed to provide more 
        comprehensive information about partners in the system
    """,
    'author': "Prosys",
    'website': "https://www.prosys-sa.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base','account','stock','sale','contacts','hr','purchase','base_geolocalize'],
    'data': [
        # 'data/data.xml',
        'security/ir.model.access.csv',
        'views/partner_activty.xml',
        'views/made_in_views.xml',
        'views/sales_view.xml',
        'views/jop_postion.xml',
        'views/regional_area.xml',
        'views/district.xml',
        'views/quantity_hand.xml',

        
        "report/sale_report_view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'posys_partner_extra_info/static/src/js/custom_inherit_wiz.js',
        ],
    },

}
