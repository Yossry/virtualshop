# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Sale Margin Report (PDF/XLS)',
    'version': '13.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Sales Management',
    'description':
        """
        This Module add below functionality into odoo

        1.Print sale margin report as pdf or excel\n
odoo sale margin
odoo sale profit
sale margin
sale margin odoo
odoo sale margin 
sale margin
sale margin odoo report
odoo margin 
odoo margin report
odoo product category margin
odoo sale margin xls 
odoo sale margin pdf report
odoo sale margin product wise
odoo sale margin product category wise
Sale Margin report 
Odoo sale margin Report 
Manage Sale Margin report 
Odoo manage sale margin report 
This Odoo application allows you to print Sale Margin Report as pdf file or you can also export it into excel sheet
This Odoo app allows you to print Sale Margin Report as pdf file or you can also export it into excel sheet
Manage This Odoo application allows you to print Sale Margin Report as pdf file or you can also export it into excel sheet
Mange This Odoo app allows you to print Sale Margin Report as pdf file or you can also export it into excel sheet
Print Sale Margin Report as pdf file
Odoo Print Sale Margin Report as pdf file
Manage Print Sale Margin Report as pdf file
Odoo manage Print Sale Margin Report as pdf file
Export Sale Margin Report into excel sheet
Odoo Export Sale Margin Report into excel sheet
Manage Export Sale Margin Report into excel sheet
Odoo manage Export Sale Margin Report into excel sheet
Filter report by Customer 
Odoo Filter report by Customer 
Manage Filter report by Customer 
Odoo manage Filter report by Customer 
Filter report by Product
Odoo Filter report by Product
Manage Filter report by Product
Odoo manage Filter report by Product
Filter report by salesperson
Odoo Filter report by salesperson
Manage Filter report by salesperson
Odoo manage Filter report by salesperson
Filter report by Company 
Odoo Filter report by company 
Manage Filter report by Company 
Manage Odoo Filter report by company 
Filter report by warehouse 
Odoo Filter report by warehouse 
Manage Filter report by warehouse 
Manage Odoo Filter report by warehouse
Filter report by sales team
Odoo Filter report by sales team
Manage Filter report by sales team
Manage Odoo Filter report by sales team
Print sale margin report 
Odoo print sale margin report 
Manage print sale margin report 
Odoo manage print sale margin report 


    """,
    'summary': 'sale margin pdf excel report, sale profit report, margin by sales team, sale margin product wise, Sales margin Product category wise, Sale Profit by Sales team, Sales margin by sales person, date wise sales margin, sales margin warehouse',
    'depends': ['sale_management', 'sale_margin', 'stock'],
    'data': [
            'wizard/export_sale_margin_view.xml',
            'report/template_sale_margin_report.xml',
            'report/menu_sale_margin_report.xml'
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':19.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
