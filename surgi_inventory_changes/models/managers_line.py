
from odoo import models ,fields

class manager_line(models.Model):
    _name = 'manager.line'
    manager_id = fields.Many2one('res.users')

    warehouse_id = fields.Many2one('stock.warehouse')
