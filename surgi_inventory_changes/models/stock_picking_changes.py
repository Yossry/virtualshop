# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning

## A.Salama .... Code Start
class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    receipt_exchange = fields.Boolean(string="Receipt Exchange? ",related='picking_type_id.receipt_exchange',
                                      help="Used ot show if type is receipt exchange or not")
    #
    type_delivery_type = fields.Selection(string="Delivery Type ",related='picking_type_id.delivery_type',
                                     selection=[('gov', 'Government Form'), ('exchange', 'Exchange ')],
                                     help="Used ot show picking type delivery type")
    tender_order_id = fields.Many2one(comodel_name='stock.picking',string="Tender Delivery Order",
                             help="used to set Tender Delivery Order",
                                      domain=[('type_delivery_type','=','exchange')])
    exchange_order_id = fields.Many2one(comodel_name='stock.picking', string="Exchange Receipt Order",
                                      help="used to set Exchange Receipt Order",
                                      domain=[('receipt_exchange', '=', True)])
    gov_form_url = fields.Char(string="Gov Form URL",help="used to add Gov Form URL")

    approval_lines=fields.One2many('approval.line','pick_id')
    
    @api.onchange('location_dest_id')
    def _get_managers(self):
        _error_mesaage=''
        for rec in self:
            if rec.location_dest_id and rec.picking_type_id.code == 'internal':
                mangers = rec.location_dest_id.warehouse_id.manager_lines
                lines=[]
                for M in mangers:
                    if(M.manager_id.name):
                        _error_mesaage+=M.manager_id.name+" "
                    # print M.manager_id.name
                    line=(0,0,{
                        'warehouse_manager_id':M.manager_id,
                        'is_approved':False,
                        'has_rule':True if M.manager_id==self.env.user else False
                        })
                    lines.append(line)
                rec.approval_lines=lines




    def do_new_transfer(self):
        print (" Lol")
        """
        on validation add this id on other exchange order
        :return: super
        """
        # Load Initial Demand
        self.save_descrip_action()
        if self.receipt_exchange:
            ## in case of recipt exchange order add it's id on tendre order
            if self.tender_order_id:
                self.tender_order_id.write({'exchange_order_id' : self.id})
        elif self.type_delivery_type == 'exchange':
            ## in case of exchange order add it's id on exhchange  order
            if self.exchange_order_id:
                self.exchange_order_id.write({'tender_order_id' : self.id})
            ## If there is no exchange order raise warning
            else:
                raise Warning ("Please Set Exchange Receipt Order to be able to validate")
        ## 1- is internal transfer
        ## 2- it's location has required_approval checkbox checked
        ## 3- it's location has warehouse, and warehouse have manager
        ## 4- it's location has warehouse, and warehouse have manager and this manager didn't check approve
        pick_approved = False
        for line in self.approval_lines:
            if line.is_approved:
                pick_approved = True
                break
        # raise Warning(pick_approved )
        if self.location_dest_id.required_approval  and \
            self.location_id.required_approval  and \
            not pick_approved:
            _error_mesaage=' '
            for rec in self:
                mangers = rec.location_dest_id.warehouse_id.manager_lines
                for M in mangers:
                    if M.manager_id.name:
                        _error_mesaage+=M.manager_id.name+" OR "
            e_message=_error_mesaage[:-3]
            message ='Please ask warehouse manager ('+e_message+' ) to approve order first'
            for x in xrange(1,10):
                pass
            raise Warning(message)
        return super(StockPickingInherit, self).do_new_transfer()
## A.Salama .... Code end.


