from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models


class stock_production_lot_inherit(models.Model):
    _inherit = 'stock.production.lot'

    @api.onchange('expiration_date')
    def get_exp_date(self):
        date = self.expiration_date
        self.life_date = date