from odoo import api, fields, models,exceptions
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        imediate_obj = self.env['stock.immediate.transfer']
        res = super(SaleOrder,self).action_confirm()
        for order in self:

            warehouse = order.warehouse_id
            if warehouse.is_delivery_set_to_done and order.picking_ids: 
                for picking in self.picking_ids:
                    picking.action_assign()
                    picking.action_confirm()
                    for mv in picking.move_ids_without_package:
                        mv.quantity_done = mv.product_uom_qty
                    picking.button_validate()
                    # picking.action_done()
                    # imediate_rec = imediate_obj.create({'pick_ids': [(4, order.picking_ids.id)]})
                    # imediate_rec.process()

            if warehouse.create_invoice and not order.invoice_ids:
                order._create_invoices()  

            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()

        return res  
