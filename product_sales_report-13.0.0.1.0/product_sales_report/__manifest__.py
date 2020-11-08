# -*- coding: utf-8 -*-
{
    'name': 'Sales Detail Report',
    'summary': "Sales report by summery, Day wise (weekly) report by sales person or Team by products or category in PDF.",
    'description': "Sales report by summery, Day wise (weekly) report by sales person or Team by products or category in PDF",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    'support': 'ipredictitsolutions@gmail.com',

    'category': 'Sales',
    'version': '13.0.0.1.0',
    'depends': ['sale_management'],

    'data': [
        'wizard/product_sales_wizard_view.xml',
        'report/product_sales_report_summary_view.xml',
        'report/product_sales_report_weekly_view.xml',
    ],

    'license': "OPL-1",
    'price': 35,
    'currency': "EUR",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/main.png'],
}
