from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models


class res_partner_inherit(models.Model):
    _inherit = 'res.partner'

    customer = fields.Boolean(string="Is a customer")
    vendor = fields.Boolean(string="Is a vendor")
    customer_kind = fields.Selection([('undefined','Undefined'),('hospital','Hospital'),('surgeon','Surgeon'),('company','Company'),('pharmacy','Pharmacy'),('lab','Lab'),('patient','Patient')])
    customer_category = fields.Selection([('taelimia','Educational Hospitals'),('private_uh','Private Universities Hospitals'),('public_uh','Public Universities Hospitals'),('military','Military Hospitals'),('insurance','Health Insurance Hospitals'),('muasasat','Almoasasat Aleilajia'),('private','Private Hospitals'),('moh','MOH'),('alhayyat','Alhayyat Hospitals'),('jihat_kharijia','Jihat Kharijia'),('alameenah','Al Ameenah Hospitals'),('individual','Individual'),('surgeon','surgeon'),('company','Private Company'),('pharmacy','Pharmacy'),('lab','Lab')])
    suregon_code = fields.Char(string="Surgeon Code", required=False)
    tareget_in_out = fields.Selection([('in','IN'),('out','OUT')],string='Tareget')
    direct_sales_users = fields.Many2many('res.users',string="Direct Sales Users")

    gender = fields.Selection([('m', 'Male'), ('f', 'Female')])
    authority = fields.Selection([
        ('closed', 'Closed'),
        ('open', 'Open'),
        ('open_approval', 'Open with Approval')
    ], string='Authority Type')
    arabic_name = fields.Char(string="Arabic Name", required=False)
