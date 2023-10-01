# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    "name": "Sale Geolocation",
    "version": "16.0.1.0",
    "category": "Sales/Sales",
    "license": "OPL-1",
    "description": "This module fetch the Geolocation of the user when it creates.",
    'summary': 'This module fetch the Geolocation of the user when it creates | geolocation on create | location | sale order location | sale order geolocation',
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "depends": ['sale_management','sale'],
    'images': ['static/description/banner.gif'],
    "data": [
        'security/sale_purchase_group.xml',
        "views/sale_view.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'sale_geolocation/static/src/js/form_controller.js',
        ]
    },
    "installable": True,
    "price": 29,
    "currency": "EUR",
}
