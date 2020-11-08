from odoo import models, fields, api, _


class transfer_validation_confirmation(models.TransientModel):
    _name = 'transfer.validation.confirmation'

    def transfer_validation_confirmed(self):
        obj = self.env['stock.picking'].search([('id', '=', self._context.get('active_ids')[0])])
        print ('++++++++++++++++++++++', obj)
        return obj.do_transfer_confirmed()
