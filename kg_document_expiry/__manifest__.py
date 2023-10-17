# -*- coding: utf-8 -*-
{
    "name": "Prosys Document Expiry",
    "summary": "Set Expiry Date for Document",
    "version": "16.0.1.0.0",
    'category': 'Productivity/Documents',
    'author': "Prosys",
    'maintainer': "Ameen",
    "license": "OPL-1",
    'website': 'https://www.prosys.com',

    "depends": ["web", "documents", "hr"],
    "data": [
        'views/email_template.xml',
        'views/documents_views.xml',
        'views/cron_jobs.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kg_document_expiry/static/src/views/inspector/documents_inspector_field.js',
            'kg_document_expiry/static/src/views/inspector/documents_inspector.js',
            'kg_document_expiry/static/src/views/inspector/documents_inspector.xml',


        ],
    },
    'images': ['static/description/logo.png'],
    "installable": True,
}
