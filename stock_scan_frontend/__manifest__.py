{
    'name': 'stock scan frontend',
    'version': '1.1',
    'summary': '',
    'category': 'stock',
    'data': [
        "stock_picking_view.xml",
    ],
    'depends': ['stock','stock_lot_scan'],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
}
