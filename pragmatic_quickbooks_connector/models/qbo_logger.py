from odoo import api, fields, models, _

class QBOLoger(models.Model):
    _name = 'qbo.logger'
    _rec_name = 'odoo_name'

    odoo_name = fields.Char('Name')
    odoo_object = fields.Char('Object')
    message = fields.Char('Message')
    created_date = fields.Datetime('Created Date')
