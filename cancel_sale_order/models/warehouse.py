from odoo import api, fields, models
class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    cancel_delivery_order = fields.Boolean(string="Cancel Delivery Order?")
    cancel_invoice=fields.Boolean(string='Cancel Invoice?')