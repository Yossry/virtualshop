from odoo import api, fields, models,exceptions
from odoo.tools.float_utils import float_round, float_compare, float_is_zero

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_cancel(self):
        quant_obj= self.env['stock.quant']
        moves = self.env['account.move']
        account_move_obj=self.env['account.move']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        for order in self:
            if order.picking_ids and order.warehouse_id.cancel_delivery_order :
                for picking in order.picking_ids:
                    if picking.state ==  'cancel':
                        continue
                    if picking.state not in ['done']:
                        picking.action_cancel()
                    else:
                        account_moves=picking.move_lines

                        for move in account_moves:
                            if move.state=='cancel':
                                continue
                            # move._do_unreserve()
                            if move.state == "done" and move.product_id.type == "product":
                                for move_line in move.move_line_ids:
                                    quantity = move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id)
                                    quant_obj._update_available_quantity(move_line.product_id, move_line.location_id, quantity,move_line.lot_id)
                                    quant_obj._update_available_quantity(move_line.product_id, move_line.location_dest_id, quantity * -1,move_line.lot_id)
                            if move.procure_method == 'make_to_order' and not move.move_orig_ids:
                                move.state = 'waiting'
                            elif move.move_orig_ids and not all(orig.state in ('done', 'cancel') for orig in move.move_orig_ids):
                                move.state = 'waiting'
                            else:
                                move.state = 'confirmed'
                            siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
                            if move.propagate_cancel:
                                # only cancel the next move if all my siblings are also cancelled
                                if all(state == 'cancel' for state in siblings_states):
                                    move.move_dest_ids._action_cancel()
                            else:
                                if all(state in ('done', 'cancel') for state in siblings_states):
                                    move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                                move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
                            account_moves = account_move_obj.search([('stock_move_id', '=', move.id)])
                            valuation = move.stock_valuation_layer_ids
                            valuation and valuation.sudo().unlink()
                            if account_moves:
                                for account_move in account_moves:
                                    account_move.button_cancel()
                                    account_move.mapped('line_ids').remove_move_reconcile()
                                    account_move.with_context(force_delete=True).unlink()

            if order.warehouse_id.cancel_invoice:
                for invoice in order.invoice_ids:
                    if invoice.journal_id and not invoice.journal_id.restrict_mode_hash_table:
                        invoice.journal_id.write({'restrict_mode_hash_table': True})
                    if invoice.state in ['draft','cancel']:
                        invoice.button_cancel()

                    else:
                        if invoice and not invoice.journal_id.restrict_mode_hash_table:
                            invoice.write({'restrict_mode_hash_table': True})
                        invoice.button_cancel()

                        

        res=super(SaleOrder,self).action_cancel()
        return res