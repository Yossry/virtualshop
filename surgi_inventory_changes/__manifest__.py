{
    'name': 'Surgitech Inventory',
    'version': '10.0.0.1',
    'category': 'Inventory',
    'description': """
Warehouse modifications
==========================
    """,
    'depends': ['stock','surgi_product_template'],
    'data': [
        'views/stock_picking_changes_view.xml',
        'views/stock_picking_type_changes_view.xml',
        'views/stock_warehouse_view_changes.xml',
        'views/stock_location_changes_view.xml',
        'views/stock_warehouse_changes_view.xml',
        'views/stock_quant_change_view.xml',
        'views/stock_move_line_changes.xml',
        'views/inventory_menu.xml',
        'security/ir.model.access.csv',
        'security/stock_inventory_security.xml',
    ],
}
