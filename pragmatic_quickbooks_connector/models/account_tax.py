# -*- coding: utf-8 -*-
import json
import logging

import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountTax(models.Model):
    _inherit = "account.tax"

    qbo_tax_id = fields.Char("QBO Tax Id", copy=False, help="QuickBooks database recordset id")
    qbo_tax_rate_id = fields.Char("QBO Tax Rate Id", copy=False, help="QuickBooks database recordset id")
    tax_agency_id = fields.Many2one('account.tax.agency', string='Agency', help="Tax agency reference")

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Inherited to add help attribute to name field"""
        res = super(AccountTax, self).fields_get(allfields, attributes=attributes)
        if 'name' in res:
            if 'help' in res['name']:
                help_str = res['name'].get('help', '') + ' In case of QBO it will accept tax code max 100 chars and tax rate max 10 chars.'
            else:
                help_str = 'In case of QBO it will accept tax code max 100 chars and tax rate max 10 chars.'
            res['name'].update({'help': help_str})
        return res

    @api.model
    def get_account_tax_ref(self, qbo_tax_id, name, type_tax_use="none"):
        tax = self.search(['&', '|', ('name', '=', name),
                           ('description', '=', name),
                           ('qbo_tax_id', '=', qbo_tax_id)], limit=1, order="id Desc")
        if not tax:
            tax = self.search(['&', '|', ('name', '=', name),
                               ('description', '=', name),
                               ('qbo_tax_rate_id', '=', qbo_tax_id)], limit=1, order="id Desc")
        if tax:
            return tax.id
        else:
            return False
            # Tax Creation code required time being skipped

    @api.model
    def get_qbo_tax_code(self, taxes):
        if len(taxes) > 1:
            raise ValidationError(_("Single composite tax required"))
        for tax in taxes:
            if tax.amount_type != 'group':
                raise ValidationError(_("Composite tax required"))
            if tax.qbo_tax_id:
                return tax.qbo_tax_id
            else:
                raise ValidationError(_("Tax not exported to QBO."))

    @api.model
    def create_account_tax(self, data):
        """Create account tax object in odoo
        :param data: account tax object response return by QBO
        :return int: last import QBO account tax Id
        """
        res = json.loads(str(data.text))
        # print("DATA : ",res)
        tax_obj = False
        if 'QueryResponse' in res:
            taxes = res.get('QueryResponse').get('TaxCode', [])
        else:
            taxes = [res.get('TaxCode')] or []
        for tax in taxes:
            _logger.info(_("\n\nTax Name : %s" % (tax.get('Name', ''))))
            _logger.info(_("Tax Id : %s" % (tax.get('Id'))))

            if tax.get('Active') == True:

                if tax.get('Taxable'):
                    vals = {
                        'name': tax.get('Name', ''),
                        'description': tax.get('Description', ''),
                        'qbo_tax_id': tax.get('Id'),
                        'amount': 0,
                        'amount_type': 'group',
                    }
                    if tax.get('TaxGroup'):
                        purchase_tax_rate_ids = []
                        sale_tax_rate_ids = []
                        # Make two different taxes for purchase and sale tax scope
                        if tax.get('PurchaseTaxRateList').get('TaxRateDetail', []):
                            for tax_rate in tax.get('PurchaseTaxRateList').get('TaxRateDetail', []):
                                purchase_tax_rate_ids.append(self.create_tax_rate(tax_rate, type_tax_use='purchase').id)
                                #                             self._cr.commit()
                            vals.update({
                                'type_tax_use': 'purchase',
                                'children_tax_ids': [(6, 0, purchase_tax_rate_ids)],
                            })
                            tax_obj = self.search([('qbo_tax_id', '=', tax.get('Id')), ('type_tax_use', '=', 'purchase')], limit=1) or self.search(
                                    [('name', '=', tax.get('Name')), ('type_tax_use', '=', 'purchase')], limit=1)
                            if not tax_obj:
                                tax_obj = self.create(vals)
                                _logger.info(_("Account tax created sucessfully! Tax Id: %s" % (tax_obj.id)))
                            else:
                                tax_obj.write(vals)
                                _logger.info(_("Account tax updated sucessfully! Tax Id: %s" % (tax_obj.id)))

                            self._cr.commit()
                            # _logger.info(_("Account tax created sucessfully! Tax Id: %s" % (tax_obj.id)))

                        if tax.get('SalesTaxRateList').get('TaxRateDetail', []):
                            for tax_rate in tax.get('SalesTaxRateList').get('TaxRateDetail', []):
                                sale_tax_rate_ids.append(self.create_tax_rate(tax_rate, type_tax_use='sale').id)
                                #                             self._cr.commit()
                            vals.update({
                                'type_tax_use': 'sale',
                                'children_tax_ids': [(6, 0, sale_tax_rate_ids)],
                            })
                            tax_obj = self.search([('qbo_tax_id', '=', tax.get('Id')), ('type_tax_use', '=', 'sale')], limit=1) or self.search(
                                    [('name', '=', tax.get('Name')), ('type_tax_use', '=', 'sale')], limit=1)
                            if not tax_obj:
                                tax_obj = self.create(vals)
                                _logger.info(_("Account tax created sucessfully! Tax Id: %s" % (tax_obj.id)))
                            else:
                                tax_obj.write(vals)
                                _logger.info(_("Account tax updated sucessfully! Tax Id: %s" % (tax_obj.id)))

                            self._cr.commit()
                            # _logger.info(_("Account tax created sucessfully! Tax Id: %s" % (tax_obj.id)))

        return tax_obj

    @api.model
    def create_tax_rate(self, tax_rate, type_tax_use='none'):
        """Create tax rate in Odoo"""
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        url_str = company.get_import_query_url()
        #         .browse(self._context.get('qbo_config_id')).get_import_query_url()
        url = url_str.get('url') + '/taxrate/%s' % tax_rate.get('TaxRateRef').get('value')
        data = requests.request('GET', url, headers=url_str.get('headers'))
        if data:
            res = json.loads(str(data.text))
            agency = False
            if 'AgencyRef' in res.get('TaxRate'):
                agency = self.env['account.tax.agency'].search([('qbo_agency_id', '=', res.get('TaxRate').get('AgencyRef').get('value'))], limit=1)
                # If tax agency is not created in odoo then import from QBO and create.
                if not agency:
                    url_str = company.get_import_query_url()
                    url = url_str.get('url') + '/taxagency/' + res.get('TaxRate').get('AgencyRef').get('value')
                    data = requests.request('GET', url, headers=url_str.get('headers'))
                    if data:
                        agency = self.env['account.tax.agency'].create_account_tax_agency(data)

            account = False
            if 'TaxReturnLineRef' in res.get('TaxRate'):
                account = self.env['account.account'].search([('qbo_id', '=', res.get('TaxRate').get('TaxReturnLineRef').get('value'))], limit=1)
                # If account is not created in odoo then import from QBO and create.
                if not account:
                    url_str = company.get_import_query_url()
                    url = url_str.get('url') + '/account/' + res.get('TaxRate').get('TaxReturnLineRef').get('value')
                    data = requests.request('GET', url, headers=url_str.get('headers'))
                    if data:
                        account = self.env['account.account'].create_account_account(data)
            # 'name': res.get('TaxRate').get('Name', '') + ' %',
            vals = {
                'name': res.get('TaxRate').get('Name', '') + ' %',
                'description': res.get('TaxRate').get('Description', ''),
                'qbo_tax_rate_id': res.get('TaxRate').get('Id'),
                'amount_type': 'percent',
                'amount': float(res.get('TaxRate').get('RateValue')),
                'type_tax_use': type_tax_use,
                'tax_agency_id': agency.id if agency else False,
                # 'account_id': account.id if account else False,
                # 'refund_account_id': account.id if account else False,
            }
            tax_obj = self.search([('qbo_tax_rate_id', '=', res.get('TaxRate').get('Id'))], limit=1)
            if not tax_obj:
                tax_obj = self.create(vals)
            else:
                print('\n\nVals : ',vals)
                tax_obj.write(vals)

            self.env.cr.commit()
            _logger.info(_("Account tax created sucessfully! Tax Id: %s" % (tax_obj.id)))
            # quickbook_config.last_imported_tax_id = res.get('TaxRate').get('Id')
            return tax_obj
        else:
            _logger.warning(_('Empty data'))

    # @api.one
    def export_tax_code_to_qbo(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        tax = self
        tax_rate_details = []
        vals = {
            'TaxCode': tax.name,
        }
        if tax.children_tax_ids:
            for child_tax in tax.children_tax_ids:
                # If child tax is not exported in QBO then export first and append return qbo id in tax_rate_ids
                if child_tax.qbo_tax_rate_id:
                    tax_rate_details.append({'TaxRateId': child_tax.qbo_tax_rate_id})
                else:
                    #                     child_tax.get_tax_rate_values(parent_tax = tax)
                    if not child_tax.tax_agency_id:
                        raise ValidationError(_("Please select tax agency for %s" % (child_tax.name)))
                    elif not child_tax.tax_agency_id.qbo_agency_id:
                        child_tax.tax_agency_id.with_context(agency_id=child_tax.tax_agency_id.id).export_to_qbo()

                    rate_vals = {
                        'TaxRateName': child_tax.name,
                        'RateValue': str(child_tax.amount),
                        'TaxAgencyId': child_tax.tax_agency_id.qbo_agency_id,
                        'TaxApplicableOn': 'Sales' if (tax.type_tax_use == 'sale') else 'Purchase',
                    }
                    tax_rate_details.append(rate_vals)
        else:
            if not tax.tax_agency_id:
                raise ValidationError(_("Please select tax agency for %s" % (tax.name)))
            elif not tax.tax_agency_id.qbo_agency_id:
                tax.tax_agency_id.with_context(agency_id=tax.tax_agency_id.id).export_to_qbo()

            rate_vals = {
                'TaxRateName': tax.name,
                'RateValue': str(tax.amount),
                'TaxAgencyId': tax.tax_agency_id.qbo_agency_id,
                'TaxApplicableOn': 'Sales' if (tax.type_tax_use == 'sale') else 'Purchase',
            }
            tax_rate_details.append(rate_vals)
        vals.update({'TaxRateDetails': tax_rate_details})
        parsed_dict = json.dumps(vals)
        if company.access_token:
            access_token = company.access_token
        if company.realm_id:
            realmId = company.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'

            result = requests.request('POST', company.url + str(realmId) + "/taxservice/taxcode", headers=headers,
                                      data=parsed_dict)
            if result.status_code == 200:
                # if not isinstance(result.text, dict):
                #     response = company.convert_xmltodict(result.text)
                #     response = response.get('IntuitResponse')
                # else:
                #     response = json.loads(result.text, encoding='utf-8')

                # update agency id and last sync id

                response = result.json()
                TaxRateDetails = response.get('TaxRateDetails', [])
                # iterating over response to map tax rate id to qbo tax rate
                for taxRate in TaxRateDetails:
                    tax_rate = self.search(['&', '|', ('name', '=', taxRate.get('TaxRateName')),
                                            ('description', '=', taxRate.get('TaxRateName')),
                                            ('qbo_tax_rate_id', '=', False)], limit=1, order="id Desc")
                    if tax_rate:
                        tax_rate.ensure_one()
                        tax_rate.qbo_tax_rate_id = taxRate.get('TaxRateId')

                tax.qbo_tax_id = response.get('TaxCodeId')
                self._cr.commit()

                if company.last_imported_tax_id < response.get('TaxCodeId'):
                    company.last_imported_tax_id = response.get('TaxCodeId')
                _logger.info(_("%s exported successfully to QBO" % (tax.name)))
            else:
                _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))
            return result

        #     @api.one
        #     def export_tax_rate_to_qbo(self, parent_tax=None):
        #         tax = self
        #         if tax.type_tax_use == 'none':
        #             raise ValidationError(_("Tax scope of '%s' should either be Sales or Purchase required"%(tax.name)))
        #         company = self.env['res.users'].search([('id','=',self._uid)],limit=1).company_id
        #         if not tax.tax_agency_id:
        #             raise ValidationError(_('Tax agency is not specified for %s'%(tax.name)))
        #         elif not tax.tax_agency_id.qbo_agency_id:
        #             raise ValidationError(_('Tax agency not available in QBO'))
        #
        #         vals = {
        #             'TaxRate': {
        #                 'Name': tax.name,
        #                 'Description': tax.description or '',
        #                 'RateValue': str(tax.amount),
        #                 'AgencyRef': {'value': tax.tax_agency_id.qbo_agency_id},
        #             },
        #         }
        #         #If refund account present in QBO then send the same reference otherwise create new in QBO and use newly created reference
        #         if tax.refund_account_id:
        #             if tax.refund_account_id.qbo_id:
        #                 qbo_id = tax.refund_account_id.qbo_id
        #             else:
        #                 qbo_id = tax.refund_account_id.export_to_qbo()
        #
        #             vals['TaxRate'].update({
        #                     'TaxReturnLineRef':{"value": qbo_id},
        #                 })
        #
        #         parsed_dict = json.dumps(vals)
        #         print "Parsed DICT IS export_tax_rate_to_qbo",parsed_dict
        #         if company.access_token:
        #             access_token = company.access_token
        #         if company.realm_id:
        #             realmId = company.realm_id
        #
        #         if access_token:
        #             headers = {}
        #             headers['Authorization'] = 'Bearer '+str(access_token)
        #             headers['Content-Type']='application/json'
        #             result = requests.request('POST',company.url+str(realmId)+"/taxservice/taxcode",headers=headers,data=parsed_dict)
        #             print "\n\n*********result***export_tax_rate_to_qbo**** ",result.status_code,result
        #             if result.status_code == 200:
        #                 print "\n\n Result =====text=== ",result.text
        #                 response = company.convert_xmltodict(result.text)
        #                 print "\n\n Result ======== ",response
        #                 #update agency id and last sync id
        #                 tax.qbo_tax_id = response.get('IntuitResponse').get('TaxCode').get('Id')
        #                 company.last_imported_tax_agency_id = response.get('IntuitResponse').get('TaxCode').get('Id')
        #                 _logger.info(_("%s exported successfully to QBO"%(tax.name)))
        #             else:
        #                 _logger.error(_("[%s] %s"%(result.status_code,result.reason)))
        #                 raise ValidationError(_("[%s] %s"%(result.status_code,result.reason)))
        #             return result

    @api.model
    def export_to_qbo(self):
        """Create account tax and tax rate in QBO"""
        #         company = self.env['res.users'].search([('id','=',self._uid)],limit=1).company_id
        if self._context.get('active_ids'):
            acc_taxes = self.env['account.tax'].browse(self._context.get('active_ids'))
        else:
            acc_taxes = self

        for tax in acc_taxes:
            # if tax.amount_type == 'group':
            tax.export_tax_code_to_qbo()
            # else:
            #     raise ValidationError(_('''Tax Computation - Group of Taxes exported to QBO with their multiple tax rate.
            #     Individual tax rate export API's is not available.'''))

    @api.model
    def export_one_tax_at_a_time(self, tax_id):
        """Create account tax and tax rate in QBO"""
        acc_taxes = tax_id
        for tax in acc_taxes:
            # if tax.amount_type == 'group':
            tax.export_tax_code_to_qbo()
            # else:
            #     raise ValidationError(_('''Tax Computation - Group of Taxes exported to QBO with their multiple tax rate.
            #         Individual tax rate export API's is not available.'''))


AccountTax()


class AccountTaxAgency(models.Model):
    _name = "account.tax.agency"
    _description = "Account tax agency used for QBO"

    qbo_agency_id = fields.Char("QBO Agency Id", copy=False, help="QuickBooks database recordset id")
    name = fields.Char("Name", required=True, help="Name of the agency.")
    tax_track_on_sale = fields.Boolean("Tax tracked on sale", default=True, help="Denotes whether this tax agency is used to track tax on sales.")
    tax_track_on_purchase = fields.Boolean("Tax tracked on purchase", help="Denotes whether this tax agency is used to track tax on purchases.")

    @api.model
    def create_account_tax_agency(self, data):
        """Create account tax object in odoo
        :param data: account tax object response return by QBO
        :return account.tax.agency: account tax agency object
        """
        res = json.loads(str(data.text))
        if 'QueryResponse' in res:
            TaxAgency = res.get('QueryResponse').get('TaxAgency', [])
        else:
            TaxAgency = [res.get('TaxAgency')] or []
        for agency in TaxAgency:
            vals = {
                'name': agency.get("DisplayName", ''),
                'qbo_agency_id': agency.get("Id"),
                'tax_track_on_sale': agency.get('TaxTrackedOnSales'),
                'tax_track_on_purchase': agency.get('TaxTrackedOnPurchases'),
            }
            agency_obj = self.create(vals)
            _logger.info(_("Tax Agency created sucessfully! Agency Id: %s" % (agency_obj.id)))
        return agency_obj

    @api.model
    def export_to_qbo(self):
        """Create account tax agency in QBO"""
        if self._context.get('agency_id'):
            agencies = self
        else:
            agencies = self.env['account.tax.agency'].browse(self._context.get('active_ids'))

        for agency in agencies:
            vals = {
                'DisplayName': agency.name,
                'TaxTrackedOnSales': agency.tax_track_on_sale,
                'TaxTrackedOnPurchases': agency.tax_track_on_purchase,
            }
            parsed_dict = json.dumps(vals)
            quickbook_config = self.env['res.users'].search([('id', '=', self._uid)], limit=1).company_id
            if quickbook_config.access_token:
                access_token = quickbook_config.access_token
            if quickbook_config.realm_id:
                realmId = quickbook_config.realm_id

            if access_token:
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(access_token)
                headers['Content-Type'] = 'application/json'

                result = requests.request('POST', quickbook_config.url + str(realmId) + "/taxagency", headers=headers, data=parsed_dict)

                if result.status_code == 200:
                    # response text is either xml string or json string
                    if isinstance(result.text, str):
                        response = quickbook_config.convert_xmltodict(result.text)
                        response = response.get('IntuitResponse')
                    else:
                        response = json.loads(result.text, encoding='utf-8')

                    # update agency id and last sync id
                    agency.qbo_agency_id = response.get('TaxAgency').get('Id')
                    quickbook_config.last_imported_tax_agency_id = response.get('TaxAgency').get('Id')

                    _logger.info(_("%s exported successfully to QBO" % (agency.name)))
                else:
                    _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                    raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))


AccountTaxAgency()
