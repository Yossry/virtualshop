from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')], string='Status',
        readonly=True, copy=False, index=True, track_visibility='onchange',
        track_sequence=3, default='draft')

    def action_confirm(self):
        '''Overright function for double validation.'''
        if self.company_id.so_double_validation == 'one_step' \
            or (self.company_id.so_double_validation == 'two_step' \
                    and self.amount_total < self.env.user.company_id.currency_id._convert(
                    self.company_id.so_double_validation_amount,
                    self.currency_id, self.company_id,
                        self.date_order or fields.Date.today())) \
            or self.user_has_groups('purchase.group_purchase_manager'):
            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(
                lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write({
                'state': 'sale',
                #'date_order': fields.Datetime.now()
            })
            self._action_confirm()
            if self.env['ir.config_parameter'].sudo().get_param(
                'sale.auto_done_setting'):
                self.action_done()
        else:
            self.write({'state': 'to approve'})
        return True
