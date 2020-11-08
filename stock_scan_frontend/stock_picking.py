from odoo import api
from odoo import fields
from odoo import models
from odoo .exceptions import Warning
import logging
class stock_picking_scan(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def scan_from_ui(self, res_id, created, added):
        logging.warning("\n Entered Form >>>>>>>>>>>>>>>>>>>>>>>>>>\ n")
        rec = self.env['stock.picking'].search([('id', '=', res_id)])
        rec.scan_products_ids.unlink()
        # print rec.scan_products_ids
        if len(created) > 0:
            for created_obj in created.values():
                for obj in created_obj.values():
                    self.env['stock.production.lot'].create(obj)

        if len(added) > 0:
            scan_lines = []
            for scan_obj in added.values():
                for obj in scan_obj.values():
                    scan_lines.append([0, 0, obj])
            rec.scan_products_ids = scan_lines