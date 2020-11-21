import json
import requests
from odoo.exceptions import ValidationError
from odoo import api, fields, models

class PaymentTermCustomization(models.Model):
    _inherit = 'account.payment.term'

    x_quickbooks_id = fields.Integer('Quickbooks ID')
    x_quickbooks_exported = fields.Boolean("Exported to Quickbooks ? ", default=False)
    x_quickbooks_updated = fields.Boolean("Updated in Quickbook ?", default=False)
    line_ids = fields.One2many('account.payment.term.line', 'payment_id', string='Terms', copy=True)

    @api.model
    def export_payment_term_to_quickbooks(self):
        # try:
            if len(self) > 1:
                raise ValidationError('Please Select 1 Record to export')
                return
            ''' Check self.name if there in quickbooks name field or not '''
            # quickbook_config = self.env['quickbook.config'].search([], limit=1)
            quickbook_config  = self.env['res.users'].search([('id', '=', 2)]).company_id

            ''' GET ACCESS TOKEN '''
            access_token = None
            realmId = None
            if quickbook_config.access_token:
                access_token = quickbook_config.access_token
            if quickbook_config.realm_id:
                realmId = quickbook_config.realm_id

            if access_token:
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(access_token)
                headers['Content-Type'] = 'application/json'
                headers['Accept'] = 'application/json'

                sql_query = "select Id,SyncToken from term Where Id = '{}'".format(self.x_quickbooks_id)

                result = requests.request('GET', quickbook_config.url + str(realmId) + "/query?query=" + sql_query, headers=headers)
                if result.status_code == 200:
                    parsed_result = result.json()
                    if parsed_result.get('QueryResponse'):
                        if parsed_result.get('QueryResponse').get('Term') and parsed_result.get('QueryResponse').get('Term')[0]:

                            dict = {}
                            ''' Record is not present in Quickbooks, Hence we can insert it '''
                            dict['Name'] = str(self.name)

                            if self.active:
                                dict['Active'] = "true"
                            else:
                                dict['Active'] = "false"

                            payment_term_line = self.env['account.payment.term.line'].search([('payment_id', '=', self.id), ('days', '!=', 0)])
                            if payment_term_line and payment_term_line.days:
                                dict['DueDays'] = payment_term_line.days

                            if self.x_quickbooks_id:
                                dict['Id'] = self.x_quickbooks_id
                                dict['sparse'] = 'true'
                                dict['SyncToken'] = parsed_result.get('QueryResponse').get('Term')[0].get('SyncToken')
                                dict = json.dumps(dict)
                                # print("==== in if dict ===",dict)
                                result = requests.request('POST', quickbook_config.url + str(realmId) + "/term?operation=update", headers=headers,
                                                          data=dict)
                                if result.status_code == 200:
                                    self.x_quickbooks_updated = True
                    else:
                        dict = {}
                        ''' Record is not present in Quickbooks, Hence we can insert it '''
                        dict['Name'] = str(self.name)
                        if self.active:
                            dict['Active'] = "true"
                        else:
                            dict['Active'] = "false"
                        payment_term_line = self.env['account.payment.term.line'].search([('payment_id', '=', self.id), ('days', '!=', 0)])
                        if payment_term_line and payment_term_line.days:
                            dict['DueDays'] = payment_term_line.days
                        dict = json.dumps(dict)
                        # print("==== in if else ===", dict)
                        result = requests.request('POST', quickbook_config.url + str(realmId) + "/term", headers=headers, data=dict)
                        if result.status_code == 200:
                            parsed_result = result.json()
                            if parsed_result.get('Term').get('Id'):
                                self.x_quickbooks_exported = True
                                self.x_quickbooks_id = parsed_result.get('Term').get('Id')
                else:
                    pass
        # except:
        #     raise ValidationError("Exception Occured")
