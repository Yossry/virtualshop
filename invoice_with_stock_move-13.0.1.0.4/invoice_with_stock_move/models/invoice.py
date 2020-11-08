# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_default_warehouse(self):
        warehouse_id = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)], limit=1)
        return warehouse_id

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', default=_get_default_warehouse)
    create_stock_moves = fields.Boolean("Create Stock Moves?", copy=False)
    picking_id = fields.Many2one('stock.picking', 'Picking', copy=False)

    #Hook: Allow to change in other module
    @api.model
    def assign_invoice_lots(self, picking):
        pass

    @api.model
    def move_line_from_invoice_lines(self, picking, location_id, location_dest_id):
        StockMove = self.env['stock.move']
        for line in self.invoice_line_ids:
            if line.product_id and line.product_id.type != 'service':
                StockMove.create({
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'date': fields.datetime.now(),
                    'date_expected': fields.datetime.now(),
                    'picking_id': picking.id,
                    'picking_type_id': picking.picking_type_id.id,
                    'state': 'draft',
                    'name': line.name,
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'quantity_done': line.quantity,
                })

    @api.model
    def create_move(self, picking_type_id, location_id, location_dest_id):
        picking_id = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'date': fields.datetime.now(), 
            'company_id': self.company_id.id,
            'picking_type_id': picking_type_id.id,
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'origin': self.name,
        })

        self.picking_id = picking_id.id
        self.move_line_from_invoice_lines(picking_id, location_id, location_dest_id)

        picking_id.action_confirm()
        picking_id.action_assign()
        self.assign_invoice_lots(picking_id)
        if picking_id.state == 'assigned':
            picking_id.with_context(default_type='entry').button_validate()


    def action_post(self):
        res = super(AccountMove, self).action_post()
        stock_location_obj = self.env['stock.location']

        for inv in self:
            if inv.create_stock_moves:
                if inv.type == 'out_invoice':
                    picking_type_id = inv.warehouse_id.out_type_id
                    location_id = inv.warehouse_id.lot_stock_id
                    location_dest_id = inv.partner_id.property_stock_customer
                    inv.create_move(picking_type_id, location_id, location_dest_id)

                if inv.type == 'in_invoice':
                    picking_type_id = inv.warehouse_id.in_type_id
                    location_id = inv.partner_id.property_stock_supplier
                    location_dest_id = inv.warehouse_id.lot_stock_id
                    inv.create_move(picking_type_id, location_id, location_dest_id)

                elif inv.type == 'out_refund':
                    picking_type_id = inv.warehouse_id.in_type_id
                    location_id = inv.partner_id.property_stock_customer
                    location_dest_id = inv.warehouse_id.lot_stock_id
                    inv.create_move(picking_type_id, location_id, location_dest_id)

                elif inv.type == 'in_refund':
                    picking_type_id = inv.warehouse_id.out_type_id
                    location_id = inv.warehouse_id.lot_stock_id
                    location_dest_id = inv.partner_id.property_stock_supplier
                    inv.create_move(picking_type_id, location_id, location_dest_id)

        return res

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        if self.picking_id:
            self.picking_id.action_cancel()