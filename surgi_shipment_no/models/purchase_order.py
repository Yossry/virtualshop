from odoo import models, fields, api,_
class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    shipment_no_ids = fields.Many2many(comodel_name="shipment.shipment", string="Shipment No.", )
    is_ship = fields.Boolean(string="",compute='calculate_shipment_no'  )

    @api.depends('shipment_no_ids', 'state', 'picking_ids')
    def calculate_shipment_no(self):
        self.is_ship = False
        for rec in self:
            for line in rec.picking_ids:
                rec.is_ship = True
                line.shipment_no_ids = rec.shipment_no_ids.ids


    def action_view_picking(self):
        """ This function returns an action that display existing picking orders of given purchase order ids. When only one found, show the picking immediately.
        """
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        # override the context to get rid of the default filtering on operation type
        result['context'] = {'default_partner_id': self.partner_id.id, 'default_origin': self.name, 'default_picking_type_id': self.picking_type_id.id}
        pick_ids = self.mapped('picking_ids')
        pick_ids.shipment_no_ids=self.shipment_no_ids.ids
        # choose the view_mode accordingly
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = pick_ids.id
        return result


class NewModule(models.Model):
    _name = 'shipment.shipment'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    shipment_no_ids = fields.Many2many(comodel_name="shipment.shipment", string="Shipment No.", )

