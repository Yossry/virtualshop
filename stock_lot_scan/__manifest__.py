{
    'name': 'Stock Lot Scan',
    'version': '1.1',
    'category': 'Sales',
    'website': '',
    'depends': ['stock', 'stock_account', 'sale', 'product'],
    'data': [

        # 'views/sale_order_changes_view.xml',

        'views/stock_picking_changes_view.xml',
        'wizard/validation_confirmation_wizard.xml',

        'security/ir.model.access.csv',

    ],
'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,

}
