from odoo import fields, models, api, exceptions


class stock_move_inherit(models.Model):
    _inherit = 'stock.move'

    u_p_usd = fields.Float(string="U. Price in USD")
