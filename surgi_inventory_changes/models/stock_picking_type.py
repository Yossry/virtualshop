# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
## A.Salama .... Code Start

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    receipt_exchange = fields.Boolean(string="Receipt Exchange? ",help="Used ot show if type is receipt exchange or not")
    delivery_type = fields.Selection(string="Delivery Type ",selection=[('gov','Government Form'),('exchange','Exchange ')],help="Used ot show delivery type")
## A.Salama .... Code end.
