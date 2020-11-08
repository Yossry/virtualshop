from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models


class scanned_products_lines(models.Model):
    _name = 'scan.product'
    _rec_name = 'product_id'
    _description = 'Scanned Products'

    product_id = fields.Many2one('product.product', string="Product")
    lot_no = fields.Char(string="Serial No.")
    product_uom_qty = fields.Float(string="Qty")
    stock_picking_id = fields.Many2one('stock.picking', string="Stock Picking")
    lot_name = fields.Char(string='Lot Name', help="Unique Serial Number")
    expiration_date = fields.Date(string="Expiration Date")
    pick_Typ_code = fields.Selection(related='stock_picking_id.pickin_Typ_code', string="Code")
    product_availabilty = fields.Integer(string="Availabilty", compute='_get_lot_source_count')

    @api.depends('lot_no')
    def _get_lot_source_count(self):
        for rec in self:
            lot_no = rec.lot_no
            product_id = rec.product_id
            location_id = rec.stock_picking_id.location_id.id
            avail = 0
            lots = self.env['stock.production.lot'].search([('name', '=', lot_no), ('product_id', '=', product_id.id)])
            if len(lots) > 0:
                for lot in lots:
                    for quant_id in lot.quant_ids:
                        quant_location_id = quant_id.location_id.id
                        if quant_location_id == location_id:
                            avail += int(quant_id.quantity)
            rec.product_availabilty = avail


class temp_products_lines(models.Model):
    _name = 'temp.product'
    _rec_name = 'product_id'
    _description = 'Temp Scanned Products'

    product_id = fields.Many2one('product.product', string="Product")
    lot_no = fields.Char(string="Serial No.")
    product_uom_qty = fields.Float(string="Qty")
    stock_picking_id = fields.Many2one('stock.picking', string="Stock Picking")
    lot_name = fields.Char(string='Lot Name', help="Unique Serial Number")
    expiration_date = fields.Date(string="Expiration Date")
    pick_Typ_code = fields.Selection(related='stock_picking_id.pickin_Typ_code', string="Code")
