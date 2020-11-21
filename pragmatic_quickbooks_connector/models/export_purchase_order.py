from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
# from openerp.exceptions import UserError, ValidationError
import requests
import json
import logging
import datetime

_logger = logging.getLogger(__name__)

class Purchase_Order(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_purchaseorder_export_line_dict(self, line):
        #         line = self
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        vals = {
            'Description': line.name,
            'Amount': line.price_subtotal,
        }

        if line.taxes_id:
            raise Warning("QBO does not have taxable purchase orders, Taxable purchase orders cannot be exported.")

        if self.partner_id.supplier_rank:

            vals.update({
                'DetailType': 'ItemBasedExpenseLineDetail',
                'ItemBasedExpenseLineDetail': {
                    'ItemRef': {'value': self.env['product.template'].get_qbo_product_ref(line.product_id)},
                    'UnitPrice': line.price_unit,
                    'Qty': line.product_qty,
                    # 'Amount': line.price_subtotal,
                    },
            })

            # product_id = self.env['product.template'].get_qbo_product_ref(line.product_id)
            # print("PRODUCT ID : -----------> ",product_id)
            # product_rec = self.env['product.template'].search([('id','=',product_id)])
            # product_acc = product_rec.property_account_income_id.id
            # account_id = self.env['account.account'].search([('id', '=', product_acc)])
            #
            # print("----------> ",product_acc,account_id.qbo_id)
            #
            # dict_acc = {"DetailType": "AccountBasedExpenseLineDetail",
            #           "AccountBasedExpenseLineDetail": {
            #           "AccountRef": {
            #             "value": account_id.qbo_id,
            #           },
            # }}
            # vals.update(dict_acc)

        # print("=================>>>>>>> ",vals)
        return vals

    @api.model
    def _prepare_purchaseorder_export_dict(self):
        vals = {
            'DocNumber': self.name,
            'TxnDate': str(self.date_order)
        }

        if self.partner_id.supplier_rank:
            vals.update({'VendorRef': {'value': self.env['res.partner'].get_qbo_partner_ref(self.partner_id)}})

        # print("\n\nDICT : ",vals)
        lst_line = []

        for line in self.order_line:
            line_vals = self._prepare_purchaseorder_export_line_dict(line)
            lst_line.append(line_vals)
        vals.update({'Line': lst_line})
        if self.partner_id.property_account_payable_id:
            account_payable = self.partner_id.property_account_payable_id
            if account_payable.qbo_id : 
                _logger.info("ACCOUNT IS SYNCED FROM QBO!")
                vals.update({"APAccountRef": {
                    "name":account_payable.name,
                    "value": account_payable.qbo_id,
                    }})
            else:
                raise ValidationError(_("Please export the Account Payable associated with vendor to QBO,and then export Purchase Order"))
        return vals

    @api.model
    def exportPurchaseOrder(self):
        """export account invoice to QBO"""
        quickbook_config = self.env['res.users'].search([('id', '=', 2)]).company_id

        if self._context.get('active_ids'):
            purchase_orders = self.browse(self._context.get('active_ids'))
        else:
            purchase_orders = self

        for purchase_order in purchase_orders:
            if len(purchase_orders) == 1:
                if purchase_order.quickbook_id:
                    raise ValidationError(_("Purchase Order is already exported to QBO. Please, export a different Purchase Order."))
            if len(purchase_orders) > 1:
                if purchase_order.quickbook_id:
                    _logger.info("Purchase order is already exported to QBO")

            if not purchase_order.quickbook_id:

                if purchase_order.state == 'purchase':
                    vals = purchase_order._prepare_purchaseorder_export_dict()
                    # print("VALUES : -------------------> ",vals)
                    # account = self.env['account.account'].search([('name', '=', 'Accounts Payable (A/P)')])
                    # print("ACCOUNT ID : --------------> ", account, account.qbo_id)
                    #
                    # vals.update({'APAccountRef': {'value':'33'}})
                    
                    parsed_dict = json.dumps(vals)
                    # print("\nDICTIONARY : ",parsed_dict)
                    if quickbook_config.access_token:
                        access_token = quickbook_config.access_token
                    if quickbook_config.realm_id:
                        realmId = quickbook_config.realm_id

                    if access_token:
                        headers = {}
                        headers['Authorization'] = 'Bearer ' + str(access_token)
                        headers['Content-Type'] = 'application/json'
                        # print("here-------------->")
                        if purchase_order.partner_id.supplier_rank:
                            # print("purchase_order.partner_id.supplier=================>",purchase_order.partner_id.supplier)
                            result = requests.request('POST', quickbook_config.url + str(realmId) + "/purchaseorder",
                                                      headers=headers, data=parsed_dict)

                            # print("\n\nRESULT ===================: ",result)
                            if result.status_code == 200:
                                response = quickbook_config.convert_xmltodict(result.text)
                                # print("RESPONSE : ---------------/> ",response)
                                # update QBO invoice id
                                if purchase_order.partner_id.supplier_rank:
                                    purchase_order.quickbook_id = response.get('IntuitResponse').get('PurchaseOrder').get('Id')
                                    self._cr.commit()
                                _logger.info(_("%s exported successfully to QBO" %(purchase_order.name)))
                            #                         return True
                            else:
                                _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                                raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))
                        #                         return False
                else:
                    if len(purchase_orders) == 1:
                        raise ValidationError(_("Only Confirmed Purchase Order is exported to QBO."))
