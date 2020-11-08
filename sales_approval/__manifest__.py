# -*- coding: utf-8 -*-
{
    'name': 'Sales Approval',
    'summary': 'Allow to approve sale order',
    'version': '13.0.0.2.3',
    'sequence': 1,
    'description': """
Sales Approval
=================
* Allow to configure double validation in Sale Order.
    """,
    'author': 'AVP Technolabs',
    'company': 'AVP Technolabs',
    'price': 29.00,
    'currency': 'USD',
    'website': 'https://www.avptechnolabs.com',
    'category': 'Sales',
    'depends': ['sale_stock', 'sale_management'],
    'license': 'OPL-1',    
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale_order_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
