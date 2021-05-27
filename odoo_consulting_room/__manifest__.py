# -*- coding: utf-8 -*-
{
    'name': "Consulting Room App",

    'summary': """
        Application allows you to enter a patient """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Carlos Alberto LEON PAITAN",

    # Categories can be used to filter modules in modules listing
    'category': 'health',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/report_views.xml',
    ],
}
