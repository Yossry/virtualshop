
from odoo import models ,fields,api

class approval_line(models.Model):
    _name = 'approval.line'

    warehouse_manager_id = fields.Many2one(comodel_name='res.users', string="Warehouse Manager",readonly=True)
    has_rule = fields.Boolean("Is Manager?" ,compute="_is_manager",readonly=True)
    is_approved = fields.Boolean("Approve?", readonly=True)

    pick_id=fields.Many2one('stock.picking',readonly=True)

    def _is_manager(self):
        for rec in self :
            # print rec.warehouse_manager_id.id
            # print self.env.user
            rec.has_rule =True if rec.warehouse_manager_id.id==self.env.user.id else False