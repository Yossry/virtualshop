# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import math
from odoo import models, fields, api, _


class ShProductTemplate(models.Model):
    _inherit = 'product.template'
    
    sh_disc_type = fields.Selection(selection=[('fix','Amount'),('per','Percentage')], string="Discount Type")
    sh_disc_val = fields.Float('Discount Value')
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.onchange('product_id','discount')
    def onchange_pro_qty(self):
        if self:
            for rec in self:
                if rec.product_id.sh_disc_type == 'fix':
                    rec.price_unit = rec.product_id.list_price
                    if rec.price_unit != 0.0:
                        dis_per = (rec.product_id.sh_disc_val/rec.price_unit)*100
                        rec.discount = dis_per
                if rec.product_id.sh_disc_type == 'per':
                    rec.discount = rec.product_id.sh_disc_val
                    