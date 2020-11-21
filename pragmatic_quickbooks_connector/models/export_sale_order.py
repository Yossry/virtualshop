from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
# from openerp.exceptions import UserError, ValidationError
import requests
import json
import logging
import datetime

_logger = logging.getLogger(__name__)

class Sales_Order(models.Model):
    _inherit = "sale.order"
    

    @api.model
    def _prepare_saleorder_export_line_dict(self, line):
        #         line = self
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        vals = {
            'Description': line.name,
            'Amount': line.price_subtotal,
        }
        
        if line.tax_id:
            raise Warning("QBO does not have taxable Sale orders, Taxable sale orders cannot be exported.")
            taxCodeRefValue = 'TAX'
            # tax = self.env['account.tax'].get_qbo_tax_code(line.tax_id)
        else:
            taxCodeRefValue = 'NON'

        if self.partner_id.customer_rank:
            vals.update({
                'DetailType': 'SalesItemLineDetail',
                'SalesItemLineDetail': {
                    'ItemRef': {'value': self.env['product.template'].get_qbo_product_ref(line.product_id)},
                    'TaxCodeRef': {'value': taxCodeRefValue},
                    'UnitPrice': line.price_unit,
                    'Qty': line.product_uom_qty,
                }
            })

        return vals

    @api.model
    def _prepare_saleorder_export_dict(self):
        vals = {
            'DocNumber': self.name,
            'TxnDate': str(self.date_order),
            # 'DueDate': self.date_due,
        }
        if self.partner_id.customer_rank:
            vals.update({'CustomerRef': {'value': self.env['res.partner'].get_qbo_partner_ref(self.partner_id)}})

        # elif invoice.partner_id.supplier:
        #     vals.update({'VendorRef': {'value': self.env['res.partner'].get_qbo_partner_ref(invoice.partner_id)}})
        total_tax_id = 0
        lst_line = []
        arr = []
        tax_id = 0
        for line in self.order_line:
            line_vals = self._prepare_saleorder_export_line_dict(line)
            lst_line.append(line_vals)
            if line.tax_id.id:

                if line.tax_id.qbo_tax_id:
                    tax_id = line.tax_id.id
                    arr.append(tax_id)
                elif not line.tax_id.qbo_tax_id:
                    exported = self.env['account.tax'].export_one_tax_at_a_time(line.tax_id)

                    is_exported = self.env['account.tax'].search([('id','=',line.tax_id.id)])
                    if is_exported:
                        if line.tax_id.qbo_tax_id:
                            tax_id = line.tax_id.id
                            arr.append(tax_id)

            # total_tax_id = total_tax_id + tax_id
            # total_tax_id_id = total_tax_id/2
            # print("TOTAL TAX : ----->  ",total_tax_id_id)
            # print("------------------->>>>>>>>> ",line.tax_id.id)
        vals.update({'Line': lst_line})

        if tax_id:
            # print("ARRAY ---------------------------->> ",arr)
            j = 0
            for i in arr:
                # print("print--------------->",j,len(arr))
                if len(arr) == 1:
                    tax_added = self.env['account.tax'].search([('id', '=', tax_id)])
                    # print("===========>", tax_added.qbo_tax_id, )

                    vals.update({"TxnTaxDetail": {
                        "TxnTaxCodeRef": {
                            "value": tax_added.qbo_tax_id
                        }}})
                if j < len(arr)-1:
                    # print("-------->",i,arr[j],arr[j+1])
                    if arr[j] == arr[j+1]:
                        # print("\n\n================>",arr[j],arr[j+1])
                        j = j + 1

                        tax_added = self.env['account.tax'].search([('id','=',tax_id)])
                        # print("===========>",tax_added.qbo_tax_id,)

                        vals.update({"TxnTaxDetail": {
                                                    "TxnTaxCodeRef": {
                                                        "value": tax_added.qbo_tax_id
                                                    }}})
                    else:
                        raise Warning("You need to add same tax for the required orderlines.")

        # print("VALS ####",vals)
        return vals

    @api.model
    def exportSaleOrder(self):
        """export account invoice to QBO"""
        quickbook_config= self.env['res.users'].search([('id', '=', 2)]).company_id

        if self._context.get('active_ids'):
            sales = self.browse(self._context.get('active_ids'))
        else:
            sales = self
        for sale in sales:
            if len(sales) == 1:
                if sale.quickbook_id:
                    _logger.info("Sale order is already exported to QBO")
                    raise Warning("Sale order is already exported to QBO")
                    # raise ValidationError(_("Sale Order is already exported to QBO. Please, export a different Sale Order."))
            if len(sales) > 1:
                if sale.quickbook_id:
                    _logger.info("Sale order is already exported to QBO")
                    raise Warning("Sale order is already exported to QBO")

            if not sale.quickbook_id:
                if sale.state in ['done','sale']:
                    vals = sale._prepare_saleorder_export_dict()
                    parsed_dict = json.dumps(vals)
                    if quickbook_config.access_token:
                        access_token = quickbook_config.access_token
                    if quickbook_config.realm_id:
                        realmId = quickbook_config.realm_id

                    if access_token:
                        headers = {}
                        headers['Authorization'] = 'Bearer ' + str(access_token)
                        headers['Content-Type'] = 'application/json'

                        if sale.partner_id.customer_rank:
                            result = requests.request('POST', quickbook_config.url + str(realmId) + "/estimate",
                                                      headers=headers, data=parsed_dict)

                        if result.status_code == 200:
                            response = quickbook_config.convert_xmltodict(result.text)
                            # print("RESPONSE : ---------------/> ",response)
                            # update QBO invoice id
                            if sale.partner_id.customer_rank:
                                sale.quickbook_id = response.get('IntuitResponse').get('Estimate').get('Id')
                                self._cr.commit()
                            _logger.info(_("%s exported successfully to QBO" %(sale.name)))
                        #                         return True
                        else:
                            self.env['qbo.logger'].create({
                                'odoo_name': sale.name,
                                'odoo_object': 'Sale Order',
                                'message': result.text,
                                'created_date': datetime.now(),
                            })
                            _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                            # raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))
                        #                         return False
                else:
                    if len(sales) == 1:
                        raise ValidationError(_("Only confirmed Sales Order is exported to QBO."))
