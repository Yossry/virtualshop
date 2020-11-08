import logging

from odoo import fields, models, api, exceptions,tools, _
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError
from itertools import groupby
from operator import itemgetter
from odoo.addons import decimal_precision as dp


class stock_move_inherit(models.Model):
    _inherit = 'stock.move'

    check_is_scanned = fields.Boolean(string="Is Scanned Product")
    lot_name = fields.Char(string='Serial Number', help="Unique Serial Number")
    expiration_date = fields.Date(string="Expiration Date")
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=False)