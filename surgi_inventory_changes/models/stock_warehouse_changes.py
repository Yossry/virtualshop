# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'
    warehouse_users = fields.Many2many('res.users', string="Users")

    warehouse_managers_id = fields.Many2one('res.users', string="Manager")
    
    manager_lines=fields.One2many('manager.line','warehouse_id')


# ================= A.Salama ==================
class stock_picking_type_changes(models.Model):
    _inherit = 'stock.picking.type'
    # add field to relate with many2many field in stock warehuse
    warehouse_users = fields.Many2many(related="warehouse_id.warehouse_users",comodel_name='res.users', string="Users")
