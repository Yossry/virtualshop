# -*- coding: utf-8 -*-
import base64
import json
import logging
from datetime import datetime, timedelta
import requests
import xmltodict
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
from xmltodict import ParsingInterrupted

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    def import_all(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))

        '''
        This function will call other functions for importing all functionalities
        '''

        # 1.For importing chart_of_accounts
        company.import_chart_of_accounts()
        _logger.info("Chart of accounts imported successfully.")
        self._cr.commit()
        # 2.For importing Account Tax
        company.import_tax()
        _logger.info("Taxes imported successfully.")
        self._cr.commit()
        # 3 For importing customers
        company.import_customers()
        _logger.info("Customers imported successfully.")
        self._cr.commit()
        # 4.For importing vendors
        company.import_vendors()
        _logger.info("Vendors imported successfully.")
        self._cr.commit()
        # 5.For importing product category
        company.import_product_category()
        _logger.info("Product Categories imported successfully.")
        self._cr.commit()
        # 6.For importing products
        company.import_product()
        _logger.info("Product imported successfully.")
        self._cr.commit()
        # 7.for importing inventory
        company.import_inventory()
        _logger.info("Inventory imported successfully.")
        self._cr.commit()

        # 8.For importing payment method
        company.import_payment_method()
        _logger.info("Payment methods imported successfully.")
        self._cr.commit()

        # 9.For importing payment terms from quickbooks
        company.import_payment_term_from_quickbooks()
        _logger.info("Payment terms imported successfully.")
        self._cr.commit()

        # 10.For importing sale order
        company.import_sale_order()
        _logger.info("Sale Orders imported successfully.")
        self._cr.commit()

        # 11.For importing invoice
        invoice_obj = self.env['account.move']
        invoice_obj.import_invoice()
        _logger.info("Invoice imported successfully.")
        self._cr.commit()

        creditmemo_obj = self.env['account.move']
        creditmemo_obj.import_credit_memo()
        _logger.info("Credit Memo imported successfully.")
        self._cr.commit()

        # 12.For importing purchase order
        company.import_purchase_order()
        _logger.info("Purchase Order imported successfully.")
        self._cr.commit()

        # 13.For importing vendor bill
        vendorbill_obj = self.env['account.move']
        vendorbill_obj.import_vendor_bill()
        _logger.info("Vendor Bills imported successfully.")
        self._cr.commit()

        # 14.For importing payment
        company.import_payment()
        _logger.info("Vendors imported successfully.")
        self._cr.commit()

        # 15.For importing bill payment
        company.import_bill_payment()
        _logger.info("Bill payments imported successfully.")
        self._cr.commit()

        # 16.For importing department
        company.import_department()
        _logger.info("Department imported successfully.")
        self._cr.commit()

        # 17.For importing Employee
        company.import_employee()
        _logger.info("Employees imported successfully.")
        self._cr.commit()
    
    def import_customer_vendor_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))

        '''
        This function will import customers and vendors from qbo
        '''
        # For importing customers
        company.import_customers()
        _logger.info("Customers imported successfully.")
        self._cr.commit()
        #For importing vendors
        company.import_vendors()
        _logger.info("Vendors imported successfully.")
        self._cr.commit()
        
    def import_product_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))

        '''
        This function will import products from qbo
        '''
        # For importing customers
        company.import_product()
        _logger.info("Products imported successfully.")
        self._cr.commit()
        
        
    def import_customer_invoice_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))

        '''
        This function will import invoices from qbo
        '''
        #For importing invoices
        invoice_obj = self.env['account.move']
        invoice_obj.import_invoice()
        _logger.info("Invoice imported successfully.")
        self._cr.commit()


    def import_purchase_order_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))

        '''
        This function will import purchase orders from qbo
        '''
        # For importing purchase order from qbo
        company.import_purchase_order()
        _logger.info("Purchase Order imported successfully.")
        self._cr.commit()
        
    def import_vendor_bill_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))
         # 13.For importing vendor bill
        vendorbill_obj = self.env['account.move']
        vendorbill_obj.import_vendor_bill()
        _logger.info("Vendor Bills imported successfully.")
        self._cr.commit()
    
    def import_customer_payment_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))
        #For importing payment
        company.import_payment()
        _logger.info("Customer Payments imported successfully.")
        self._cr.commit()
    
    def import_vendor_payment_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Cron company is-> {}".format(company))
        #.For importing bill payment
        company.import_bill_payment()
        _logger.info("Bill payments imported successfully.")
        self._cr.commit()
        
    def export_customer_vendor_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_customers()
        company.export_vendors()
        # company.export_products()

    def export_product_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_products()

    # def export_account_cron(self):
    #     company = self.env['res.users'].search([('id', '=', 2)]).company_id
    #     company.export_accounts()
    #     company.tax()

    def export_saleorder_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_sale_order()
        
    def export_purchaseorder_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_purchase_order()
        
    def export_customer_invoice_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_invoice()
        
    def export_vendor_bill_cron(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        company.export_vendor_bill()
        

    def import_invoice_custom(self):
        invoice_obj = self.env['account.move']
        invoice_obj.import_invoice()
        _logger.info("Invoice imported successfully.")
        self._cr.commit()

    def import_credit_memo_custom(self):
        creditmemo_obj = self.env['account.move']
        creditmemo_obj.import_credit_memo()
        _logger.info("Credit Memo imported successfully.")
        self._cr.commit()

    def import_vendor_bill_custom(self):
        vendorbill_obj = self.env['account.move']
        vendorbill_obj.import_vendor_bill()
        _logger.info("Vendor Bill imported successfully.")
        self._cr.commit()

    @api.model
    def convert_xmltodict(self, response):
        """Return dictionary object"""
        try:
            # convert xml response to OrderedDict collections, return collections.OrderedDict type
            # print("Response :  ",response)
            if type(response) != dict:
                order_dict = xmltodict.parse(response)
            else:
                order_dict = response
        except ParsingInterrupted as e:
            _logger.error(e)
            raise e
        # convert OrderedDict to regular dictionary object
        response_dict = json.loads(json.dumps(order_dict))
        return response_dict

    # Company level QuickBooks Configuration fields
    client_id = fields.Char('Client Id', copy=False, help="The client ID you obtain from the developer dashboard.")
    client_secret = fields.Char('Client Secret', copy=False, help="The client secret you obtain from the developer dashboard.")

    auth_base_url = fields.Char('Authorization URL', default="https://appcenter.intuit.com/connect/oauth2", help="User authenticate uri")
    access_token_url = fields.Char('Authorization Token URL', default="https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
                                   help="Exchange code for refresh and access tokens")
    request_token_url = fields.Char('Redirect URL', default="http://localhost:5000/get_auth_code",
                                    help="One of the redirect URIs listed for this project in the developer dashboard.")
    url = fields.Char('API URL', default="https://sandbox-quickbooks.api.intuit.com/v3/company/",
                      help="Intuit API URIs, use access token to call Intuit API's")

    # used for api calling, generated during authorization process.
    realm_id = fields.Char('Company Id/ Realm Id', copy=False, help="A unique company Id returned from QBO", company_dependent=True)
    auth_code = fields.Char('Auth Code', copy=False, help="An authenticated code", company_dependent=True)
    access_token = fields.Char('Access Token', copy=False, company_dependent=True,
                               help="The token that must be used to access the QuickBooks API. Access token expires in 3600 seconds.")
    minorversion = fields.Char('Minor Version', copy=False, default="8", help="QuickBooks minor version information, used in API calls.")
    access_token_expire_in = fields.Datetime('Access Token Expire In', copy=False, help="Access token expire time.")
    qbo_refresh_token = fields.Char('Refresh Token', copy=False, company_dependent=True,
                                    help="The token that must be used to access the QuickBooks API. Refresh token expires in 8726400 seconds.")
    refresh_token_expire_in = fields.Datetime('Refresh Token Expire In', copy=False, help="Refresh token expire time.")

    #     '''  Tracking Fields for Customer'''
    #     x_quickbooks_last_customer_sync = fields.Datetime('Last Synced On', copy=False,)
    #     x_quickbooks_last_customer_imported_id = fields.Integer('Last Imported ID', copy=False,)
    '''  Tracking Fields for Account'''
    # last_customer_imported_id = fields.Char('Last Imported Customer Id', copy=False, default=0)
    last_acc_imported_id = fields.Char('Last Imported Account Id', copy=False, default=0)
    last_imported_tax_id = fields.Char('Last Imported Tax Id', copy=False, default=0)
    last_imported_tax_agency_id = fields.Char('Last Imported Tax Agency Id', copy=False, default=0)
    last_imported_product_category_id = fields.Char('Last Imported Product Category Id', copy=False, default=0)
    last_imported_product_id = fields.Char('Last Imported Product Id', copy=False, default=0)
    last_imported_customer_id = fields.Char('Last Imported Customer Id', copy=False, default=0)
    last_imported_vendor_id = fields.Char('Last Imported Vendor Id', copy=False, default=0)
    last_imported_payment_method_id = fields.Char('Last Imported Payment Method Id', copy=False, default=0)
    last_imported_payment_id = fields.Char('Last Imported Payment Id', copy=False, default=0)
    last_imported_bill_payment_id = fields.Char('Last Imported Bill Payment Id', copy=False, default=0)
    quickbooks_last_employee_imported_id = fields.Integer('Last Employee Id')
    quickbooks_last_dept_imported_id = fields.Integer('Last Department Id')
    quickbooks_last_sale_imported_id = fields.Integer('Last Sale Order Id')
    quickbooks_last_invoice_imported_id = fields.Integer('Last Invoice Id')
    quickbooks_last_purchase_imported_id = fields.Integer('Last Purchase Order Id')
    quickbooks_last_vendor_bill_imported_id = fields.Integer('Last Vendor Bill Id')
    quickbooks_last_credit_note_imported_id= fields.Integer('Last Credit Note Id')
    start = fields.Integer('Start', default=1)
    limit = fields.Integer('Limit', default=100)
    '''  Tracking Fields for Payment Term'''
    x_quickbooks_last_paymentterm_sync = fields.Datetime('Last Synced On', copy=False)
    x_quickbooks_last_paymentterm_imported_id = fields.Integer('Last Imported ID', copy=False)

    # suppress_warning = fields.Boolean('Suppress Warning', default=False, copy=False,help="If you all Suppress Warnings,all the warnings will be suppressed and logs will be created instead of warnings")
    qbo_domain = fields.Selection([('sandbox', 'Sandbox'), ('production', 'Production')],
                                  string='QBO Domain', default='sandbox')
    qb_account_recievable=fields.Many2one('account.account','Account Recievable')
    qb_account_payable=fields.Many2one('account.account','Account Payable')
    qb_income_account = fields.Many2one('account.account','Income Account')
    qb_expense_account=fields.Many2one('account.account','Expense Account')

    #setting up the Account Receivable for Partners
    @api.onchange('qb_account_recievable')
    def onchange_qb_account_recievable(self):
        acc_dict={}
        acc_dict.update({'name':'property_account_receivable_id'})
        model_id = self.env['ir.model'].search([('name','=','Contact')])
        if model_id:
            field_id = self.env['ir.model.fields'].search([('name','=','property_account_receivable_id'),('field_description','=','Account Receivable'),('model_id','=',model_id.id)])
            if field_id:
                acc_dict.update({'fields_id':field_id[0].id})
        account_id = self.env['account.account'].search([('name','=',self.qb_account_recievable.name)])
        if account_id:
            acc_dict.update({'value_reference':'account.account,'+str(account_id[0].id)})
        if acc_dict:
            # if  not self.qb_account_recievable:
            self.env['ir.property'].create(acc_dict)
#         else:
#             raise ValidationError(_('You have already set Account Receivable !changing it may cause inconsistency'))


    #Setting Up the Account Payable for Partners
    @api.onchange('qb_account_payable')
    def onchange_qb_account_payable(self):
        ap_dict={}
        ap_dict.update({'name':'property_account_payable_id'})
        model_id = self.env['ir.model'].search([('name','=','Contact')])
        if model_id:
            field_id = self.env['ir.model.fields'].search([('name','=','property_account_payable_id'),('field_description','=','Account Payable'),('model_id','=',model_id.id)])
            if field_id:
                ap_dict.update({'fields_id':field_id[0].id})
        account_id = self.env['account.account'].search([('name','=',self.qb_account_payable.name)])
        if account_id:
            ap_dict.update({'value_reference':'account.account,'+str(account_id[0].id)})
        # if  not self.qb_account_payable:
        if ap_dict:
            self.env['ir.property'].create(ap_dict)
#         else:
#             raise ValidationError(_('You have already set Account Payable !changing it may cause inconsistency'))

    #Setting Up the Income Account for Product Category
    @api.onchange('qb_income_account')
    def onchange_qb_income_account(self):
        in_dict={}
        in_dict.update({'name':'property_account_income_categ_id'})
        model_id = self.env['ir.model'].search([('name','=','Product Category')])
        if model_id:
            field_id = self.env['ir.model.fields'].search([('name','=','property_account_income_categ_id'),('field_description','=','Income Account'),('model_id','=',model_id.id)])
            if field_id:
                in_dict.update({'fields_id':field_id[0].id})
        account_id = self.env['account.account'].search([('name','=',self.qb_income_account.name)])
        if account_id:
            in_dict.update({'value_reference':'account.account,'+str(account_id[0].id)})
        if  in_dict:
            self.env['ir.property'].create(in_dict)
#         else:
#             raise ValidationError(_('You have already set Income Account !changing it may cause inconsistency'))


    #Setting Up the Expense Account for Product Category
    @api.onchange('qb_expense_account')
    def onchange_qb_expense_account(self):
        ex_dict={}
        ex_dict.update({'name':'property_account_expense_categ_id'})
        model_id = self.env['ir.model'].search([('name','=','Product Category')])
        if model_id:
            field_id = self.env['ir.model.fields'].search([('name','=','property_account_expense_categ_id'),('field_description','=','Expense Account'),('model_id','=',model_id.id)])
            if field_id:
                ex_dict.update({'fields_id':field_id[0].id})
        account_id = self.env['account.account'].search([('name','=',self.qb_expense_account.name)])
        if account_id:
            ex_dict.update({'value_reference':'account.account,'+str(account_id[0].id)})
        if  ex_dict:
            self.env['ir.property'].create(ex_dict)
        else:
            raise ValidationError(_('You have already set Expense Account !changing it may cause inconsistency'))



    # @api.multi
    def login(self):
        if not self.client_id:
            raise Warning('Please add your Client Id')
        url = self.auth_base_url + '?client_id=' + self.client_id + '&scope=com.intuit.quickbooks.accounting&redirect_uri=' + self.request_token_url + '&response_type=code&state=abccc'

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    @api.model
    def _run_refresh_token(self, **kwag):
        self.refresh_token()

    # @api.multi
    def refresh_token(self):
        """Get new access token from existing refresh token"""
        company_id = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("COMPANY ID IS  --------------> {}".format(company_id))

#         company_id = self.env['res.users'].search([('id', '=', self.env.uid)]).company_id
        if not company_id:
            company_id = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company_id:
            client_id = company_id.client_id
            client_secret = company_id.client_secret
            raw_b64 = str(client_id + ":" + client_secret)
            raw_b64 = raw_b64.encode('utf-8')
            converted_b64 = base64.b64encode(raw_b64).decode('utf-8')
            auth_header = 'Basic ' + converted_b64
            headers = {}
            headers['Authorization'] = str(auth_header)
            headers['accept'] = 'application/json'
            payload = {'grant_type': 'refresh_token', 'refresh_token': company_id.qbo_refresh_token}
            _logger.info("Payload is --------------> {}".format(payload))
            access_token = requests.post(company_id.access_token_url, data=payload, headers=headers)
            _logger.info("Access token is --------------> {}".format(access_token.text))
            if access_token:
                parsed_token_response = json.loads(access_token.text)
                _logger.info("Parsed response is ------------------> {}".format(parsed_token_response))
                if parsed_token_response:
                    company_id.write({
                        'access_token': parsed_token_response.get('access_token'),
                        'qbo_refresh_token': parsed_token_response.get('refresh_token'),
                        'access_token_expire_in': datetime.now() + timedelta(seconds=parsed_token_response.get('expires_in')),
                        'refresh_token_expire_in': datetime.now() + timedelta(seconds=parsed_token_response.get('x_refresh_token_expires_in'))
                    })
                    _logger.info(_("Token refreshed successfully!"))

    @api.model
    @api.onchange('qbo_domain')
    def onchange_qbo_domain(self):
        if self.qbo_domain == 'sandbox':
            self.url = 'https://sandbox-quickbooks.api.intuit.com/v3/company/'
        else:
            self.url = 'https://quickbooks.api.intuit.com/v3/company/'

    @api.model
    def get_import_query_url(self):
        if self.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(self.access_token)
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'
            if self.url:
                url = str(self.url) + str(self.realm_id)
            else:
                raise ValidationError(_('Url not configure'))
            return {'url': url, 'headers': headers, 'minorversion': self.minorversion}
        else:
            raise ValidationError(_('Invalid access token'))

    # @api.multi
    def import_customers(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Company is   :-> {} ".format(company))
        query = "select * from Customer WHERE Id > '%s' order by Id STARTPOSITION %s MAXRESULTS %s " % (company.last_imported_customer_id, company.start, company.limit)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'), verify=False)
        _logger.info("Customer data is *************** {}".format(data.text))
        if data:
            _logger.info("Customer data is ------------> {}".format(data))
            partner = self.env['res.partner'].create_partner(data, is_customer=True)

            if partner:
                company.last_imported_customer_id = partner.qbo_customer_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_vendors(self):
#         self.ensure_one()
        company = self.env['res.company'].search([('id', '=', 1)], limit=1)
        query = "select * from vendor WHERE Id > '%s' order by Id" % (company.last_imported_vendor_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        if data:
            _logger.info("Vendor data is ---------------> {}".format(data.text))
            # partner = self.env['res.partner'].create_vendor(data, is_vendor=True)
            partner = self.env['res.partner'].create_partner(data, is_vendor=True)
            if partner:
                self.last_imported_vendor_id = partner.qbo_vendor_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_chart_of_accounts(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
#         self.ensure_one()
        query = "select * from Account WHERE Id > '%s' order by Id" % (company.last_acc_imported_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?query=' + query
        data = requests.request('GET', url, headers=url_str.get('headers'))

        if data:
            _logger.info("Charts of accounts data is ----------------> {}".format(data))

            acc = self.env['account.account'].create_account_account(data)
            if acc:
                self.last_acc_imported_id = acc.qbo_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_tax(self):
#         self.ensure_one()
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        query = "select * From TaxCode WHERE Id > '%s' order by Id" % (company.last_imported_tax_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?query=' + query
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("Tax data is ---------------> {}".format(data))
        if data:
            acc_tax = self.env['account.tax'].create_account_tax(data)
            if acc_tax:
                company.last_imported_tax_id = acc_tax.qbo_tax_id or acc_tax.qbo_tax_rate_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_tax_agency(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
#         self.ensure_one()
        query = "select * From TaxAgency WHERE Id > '%s' order by Id" % (company.last_imported_tax_agency_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?query=' + query
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("Tax agency data is ---------------> {}".format(data))

        if data:
            agency = self.env['account.tax.agency'].create_account_tax_agency(data)
            if agency:
                self.last_imported_tax_agency_id = agency.qbo_agency_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_product_category(self):
#         self.ensure_one()
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        query = "select * from Item where Id > '%s' order by Id" % (company.last_imported_product_category_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("Product category  data is ---------------> {}".format(data))

        if data:

#             income_account_id = self.env['account.account'].get_account_ref(val)
#             print("income acc id ****************",income_account_id)
            category = self.env['product.category'].create_product_category(data)
            if category:
                company.last_imported_product_category_id = category.qbo_product_category_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_product(self):
#         self.ensure_one()
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        query = "select * from Item where Id > '%s' order by Id STARTPOSITION %s MAXRESULTS %s  " % (company.last_imported_product_id, company.start, company.limit)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("Product Data is --------------------> {}".format(data))
        if data:
            product = self.env['product.template'].create_product(data)
            _logger.info("product is ******************* {}".format(product))
            if product:
                company.last_imported_product_id = product.qbo_product_id
        else:
            _logger.warning(_('Empty data in product!!!!!'))

    # @api.multi
    def import_inventory(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("COMPANY CATEGORY IS-------------> {} ".format(company))
#         self.ensure_one()
        try:
            query = "select * from Item"
            url_str = company.get_import_query_url()
            url = url_str.get('url') + '/query?%squery=%s' % (
                'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
            data = requests.request('GET', url, headers=url_str.get('headers'))
            parsed_data = data.json()
            _logger.info("Inventory data is -----------------> {}".format(parsed_data))
            for recs in parsed_data.get("QueryResponse").get('Item'):
                _logger.info("ID IS  ---> {}".format(recs.get('Id')))
                product_exists = self.env['product.product'].search([('qbo_product_id', '=', recs.get('Id'))])
                _logger.info("Product exists -----------> {}".format(product_exists))
                if product_exists and product_exists.type == 'product':
                    _logger.info("For creation of products")
                    if product_exists.qty_available != recs.get('QtyOnHand') and recs.get('QtyOnHand') >= 0:
                        #                         product_product_id = self.env['product.product'].search([('product_tmpl_id','=',product_exists.id)]).id
                        stock_qty = self.env['stock.quant'].search([('product_id', '=', product_exists.id)])
                        _logger.info("Stock quantity is ------------->{}".format(stock_qty))
                        stock_change_qty = self.env['stock.change.product.qty']
                        vals = {
                            'product_id': product_exists.id,
                            'new_quantity': recs.get('QtyOnHand'),
                            'product_tmpl_id':product_exists.product_tmpl_id.id
                        }
                        _logger.info("vals are ------->{}".format(vals))
                        res = stock_change_qty.create(vals)
                        _logger.info("RES IS ----------->{}".format(res))
                        res.change_product_qty()
                        company.last_imported_product_id = product_exists.qbo_product_id
                        #                         stock_inventory = self.env['stock.inventory'].search([('product_id','=',product_product_id)])
                        #                         res2 = stock_inventory.write({
                        #                                               'name':"INV:" +product_exists.name+"(QBO Inventory Updated)",
                        #                                               })
        except Exception as e:
            raise ValidationError(_('Inventory Update Failed due to %s' % str(e)))

    # @api.multi
    def import_payment_method(self):
#         self.ensure_one()
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        query = "select * From PaymentMethod WHERE Id > '%s' order by Id" % (company.last_imported_payment_method_id)
        url_str = self.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("\n\n\n\n\nPayment method data is ---------------> {}".format(data.text))

        if data:
            method = self.env['account.journal'].create_payment_method(data)
            if method:
                company.last_imported_payment_method_id = method.qbo_method_id
        else:
            _logger.warning(_('Empty data'))

    def import_payment(self):
        company = self.env['res.company'].search([('id', '=', 1)], limit=1)

#         self.ensure_one()
        query = "select * From Payment WHERE Id > '%s' order by Id" % (company.last_imported_payment_id)
        url_str = self.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info("Payment data is ---------------> {}".format(data))

        if data:
            _logger.info("Data for importing customer payments in odoo is ---> {}".format(data))
            payment = self.env['account.payment'].create_payment(data, is_customer=True)
            if payment:
                company.last_imported_payment_id = payment.qbo_payment_id
        else:
            _logger.warning(_('Empty data'))

    # @api.multi
    def import_bill_payment(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

#         self.ensure_one()
        query = "select * From billpayment WHERE Id > '%s' order by Id" % (company.last_imported_bill_payment_id)
        url_str = company.get_import_query_url()
        url = url_str.get('url') + '/query?%squery=%s' % (
            'minorversion=' + url_str.get('minorversion') + '&' if url_str.get('minorversion') else '', query)
        data = requests.request('GET', url, headers=url_str.get('headers'))
        _logger.info(" Bill payment data is -----------------> {}".format(data))
        if data:
            payment = self.env['account.payment'].create_payment(data, is_vendor=True)
            if payment:
                company.last_imported_bill_payment_id = payment.qbo_bill_payment_id
        else:
            _logger.warning(_('Empty data'))

    def import_payment_term_from_quickbooks(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        payment_term = self.env['account.payment.term']

        payment_term_line = self.env['account.payment.term.line']

        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(self.access_token)
            headers['Accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'
            data = requests.request('GET', company.url + str(company.realm_id) + "/query?query=select * from term where Id > '{}'".format(
                str(company.x_quickbooks_last_paymentterm_imported_id)), headers=headers)
            if data:
                ''' Holds quickbookIds which are inserted '''
                recs = []
                parsed_data = json.loads(str(data.text))
                if parsed_data:
                    _logger.info("Payment term from qbo data is ---------------> {}".format(parsed_data))

                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Term'):
                        for term in parsed_data.get('QueryResponse').get('Term'):
                            dict = {}
                            dict_ptl = {}
                            exists = payment_term.search([('name', '=', term.get('Name'))])
                            if not exists:
                                ''' Loop and create Data '''
                                if term.get('Active'):
                                    dict['active'] = term.get('Active')
                                if term.get('Name'):
                                    dict['note'] = term.get('Name')
                                    dict['name'] = term.get('Name')
                                '''  Insert data in account payment term line and attach its id to payment term create'''
                                if term.get('DueDays'):
                                    dict_ptl['value'] = 'balance'
                                    dict_ptl['days'] = term.get('DueDays')
                                payment_term_create = payment_term.create(dict)
                                if payment_term_create:
                                    payment_term_create.x_quickbooks_id = term.get('Id')
                                    recs.append(term.get('Id'))
                                    #                                     self.x_quickbooks_last_paymentterm_imported_id = term.get('Id')
                                    company.x_quickbooks_last_paymentterm_sync = fields.datetime.now()

                                    dict_ptl['payment_id'] = payment_term_create.id
                                    payment_term_line_create = payment_term_line.create(dict_ptl)
                                    if payment_term_line_create:
                                        company.x_quickbooks_last_paymentterm_imported_id = max(recs)

                                        _logger.info(_("Payment term line was created %s" % payment_term_line_create.id))

                            else:
                                _logger.info(_("REC Exists %s" % term.get('Name')))
                            _logger.info("Records are -----------> {}".format(recs))
                            if recs:
                                company.x_quickbooks_last_paymentterm_imported_id = max(recs)

                                #     def createOdooParentId(self, quickbook_id):

    # if quickbook_id:
    #             ''' GET DICTIONARY FROM QUICKBOOKS FOR CREATING A DICT '''
    #             if self.access_token:
    #                 headers = {}
    #                 headers['Authorization'] = 'Bearer '+str(self.access_token)
    #                 headers['accept'] = 'application/json'
    #                 headers['Content-Type']='text/plain'
    #                 print "New header is :",headers
    #             data = requests.request('GET',self.url+str(self.realm_id)+'/customer/'+str(quickbook_id),headers=headers)
    #             if data:
    #                 parsed_data = json.loads(str(data.text))
    #                 cust = parsed_data.get('Customer')
    #                 if cust:
    #                     print "CCCCCCCCCC", cust
    # #                     if int(cust.get('Id')) > self.x_quickbooks_last_customer_imported_id:
    #                     print cust.get('Id'),"\n ------------------------------------------------"
    #                     ''' Check if the Id from Quickbook is present in odoo or not if present
    #                     then dont insert, This will avoid duplications'''
    #                     res_partner = self.env['res.partner'].search([('display_name','=',cust.get('DisplayName'))],limit=1)
    #
    #                     print "RRRRRRRRRRRR", res_partner
    #                     if res_partner:
    #                         return res_partner.id
    #                     if not res_partner:
    #                         print "Inside res_partner !!!!!!!!!!!!!"
    #                         dict = {}
    #                         if cust.get('PrimaryPhone'):
    #                             dict['phone'] = cust.get('PrimaryPhone').get('FreeFormNumber')
    #                         if cust.get('PrimaryEmailAddr'):
    #                             dict['email'] = cust.get('PrimaryEmailAddr').get('Address', ' ')
    #                         if cust.get('GivenName') and cust.get('FamilyName',' '):
    #                             dict['name'] = cust.get('GivenName')+" "+cust.get('FamilyName',' ')
    #                         if cust.get('GivenName') and not cust.get('FamilyName'):
    #                             dict['name'] = cust.get('GivenName')
    #                         if cust.get('FamilyName') and not cust.get('GivenName'):
    #                             dict['name'] = cust.get('FamilyName')
    #                         if not cust.get('FamilyName') and not cust.get('GivenName'):
    #                             if cust.get('CompanyName'):
    #                                 dict['name'] = cust.get('CompanyName')
    #
    # #                             if cust.get('Active'):
    # #                                 if str(cust.get('Active')) == 'true':
    # #                                     dict['active']=True
    # #                                 else:
    # #                                     dict['active']=False
    #                         if cust.get('Id'):
    #                             dict['x_quickbooks_id'] = cust.get('Id')
    #                         if cust.get('Notes'):
    #                             dict['comment'] = cust.get('Notes')
    #                         if cust.get('BillWithParent'):
    #                             dict['company_type'] = 'company'
    #                         if cust.get('Mobile'):
    #                             dict['mobile'] = cust.get('Mobile').get('FreeFormNumber')
    #                         if cust.get('Fax'):
    #                             dict['fax'] = cust.get('Fax').get('FreeFormNumber')
    #                         if cust.get('WebAddr'):
    #                             dict['website'] = cust.get('WebAddr').get('URI')
    #                         if cust.get('Title'):
    #                             ''' If Title is present then first check in odoo if title exists or not
    #                             if exists attach Id of tile else create new and attach its ID'''
    #                             dict['title'] = self.attachCustomerTitle(cust.get('Title'))
    # #                                 print "FINAL DICT TITLE IS :",dict['name'],dict['title']
    # #                                 aaaaaaaaaa
    #                         dict['company_type']='company'
    #                         print "DICT TO ENTER IS : {}".format(dict)
    #                         create = res_partner.create(dict)
    #                         if create:
    #                             if cust.get('BillAddr'):
    #                                 ''' Getting BillAddr from quickbooks and Checking
    #                                     in odoo to get countryId, stateId and create
    #                                     state if not exists in odoo
    #                                     '''
    #                                 dict = {}
    #                                 '''
    #                                 Get state id if exists else create new state and return it
    #                                 '''
    #                                 if cust.get('BillAddr').get('CountrySubDivisionCode'):
    #                                     state_id = self.attachCustomerState(cust.get('BillAddr').get('CountrySubDivisionCode'),cust.get('BillAddr').get('Country'))
    #                                     if state_id:
    #                                         dict['state_id'] = state_id
    #                                     print "STATE ID IS ::::::::::",state_id
    #
    #                                 country_id = self.env['res.country'].search([
    #                                                                         ('name','=',cust.get('BillAddr').get('Country'))],limit=1)
    #                                 if country_id:
    #                                     dict['country_id'] = country_id.id
    #                                 dict['parent_id'] = create.id
    #                                 dict['type'] = 'invoice'
    #                                 dict['zip'] = cust.get('BillAddr').get('PostalCode',' ')
    #                                 dict['city'] = cust.get('BillAddr').get('City')
    #                                 dict['street'] = cust.get('BillAddr').get('Line1')
    #                                 print "DICT IS ",dict
    #                                 child_create = res_partner.create(dict)
    #                                 if child_create:
    #                                     print "Child Created BillAddr"
    #                             if cust.get('ShipAddr'):
    #                                 ''' Getting BillAddr from quickbooks and Checking
    #                                     in odoo to get countryId, stateId and create
    #                                     state if not exists in odoo
    #                                     '''
    #                                 dict = {}
    #                                 if cust.get('ShipAddr').get('CountrySubDivisionCode'):
    #                                     state_id = self.attachCustomerState(cust.get('ShipAddr').get('CountrySubDivisionCode'),cust.get('ShipAddr').get('Country'))
    #                                     if state_id:
    #                                         dict['state_id'] = state_id
    #                                     print "STATE ID IS ::::::::::",state_id
    #
    #
    #                                 country_id = self.env['res.country'].search([('name','=',cust.get('ShipAddr').get('Country'))])
    #                                 if country_id:
    #                                     dict['country_id'] = country_id[0].id
    #                                 dict['parent_id'] = create.id
    #                                 dict['type'] = 'delivery'
    #                                 dict['zip'] = cust.get('ShipAddr').get('PostalCode',' ')
    #                                 dict['city'] = cust.get('ShipAddr').get('City')
    #                                 dict['street'] = cust.get('ShipAddr').get('Line1')
    #                                 print "DICT IS ",dict
    #                                 child_create = res_partner.create(dict)
    #                                 if child_create:
    #                                     print "Child Created ShipAddr"
    #                                 print "Created Parent"
    #                                 self.x_quickbooks_last_customer_sync = fields.Datetime.now()
    #                                 self.x_quickbooks_last_customer_imported_id = int(cust.get('Id'))
    #                             return create.id
    #
    #     def attachCustomerTitle(self, title):
    #         res_partner_tile = self.env['res.partner.title']
    #         title_id = False
    #         if title:
    #             title_id = res_partner_tile.search([('name', '=', title)], limit=1)
    #             if not title_id:
    #                 ''' Create New Title in Odoo '''
    #                 create_id = res_partner_tile.create({'name': title})
    #                 create_id = title_id.id
    #                 if create_id:
    #                     return create_id.id
    #         print "TITLE IS LLLLLLLLLLLLLL",title_id
    #         return title_id.id
    #
    #     def attachCustomerState(self, state, country):
    #         res_partner_country = self.env['res.country']
    #         res_partner_state = self.env['res.country.state']
    #         state_id = False
    #         if state and country:
    #             country_id = res_partner_country.search([('name','=',country)],limit=1)
    #             if country_id:
    #                 print "Country Id is ::",country_id.name,country_id.id
    #                 state_id = res_partner_state.search([('name','=',state)],limit=1)
    #                 print "STATE ID ::::::::::::::::",state_id.country_id.id,country_id[0].id
    #                 if state_id and state_id[0].country_id.id == country_id[0].id:
    #                     print "Found State_id ",state_id
    #                     return state_id[0].id
    #                 else:
    #                     print "Inside Else"
    #                     ''' Create New State Under Country Id '''
    #                     new_state_id = res_partner_state.create({
    #                         'country_id':country_id[0].id,
    #                         'code':state[:2],
    #                         'name':state
    #                         })
    #                     if new_state_id:
    #                         print "Created new State id",new_state_id
    #                         return new_state_id.id
    #
    #     @api.multi
    #     def importcust(self):
    #         if self.access_token:
    #             headers = {}
    #             headers['Authorization'] = 'Bearer '+str(self.access_token)
    #             headers['accept'] = 'application/json'
    #             headers['Content-Type']='text/plain'
    #             print "New header is :",headers
    #             data = requests.request('GET',self.url+str(self.realm_id)+"/query?query=select * from customer where Id > '{}'".format(self.x_quickbooks_last_customer_imported_id),headers=headers)
    #             if data:
    #                 recs = []
    #                 parsed_data = json.loads(str(data.text))
    #                 if parsed_data:
    #                     print "\n\n =======Ress====== ", parsed_data,type(parsed_data)
    #                     if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Customer'):
    #                         for cust in parsed_data.get('QueryResponse').get('Customer'):
    #         #                     if int(cust.get('Id')) > self.x_quickbooks_last_customer_imported_id:
    #                             print cust.get('Id'),"\n ------------------------------------------------"
    #                             ''' Check if the Id from Quickbook is present in odoo or not if present
    #                             then dont insert, This will avoid duplications'''
    #                             res_partner = self.env['res.partner'].search([('x_quickbooks_id','=',int(cust.get('Id')))])
    #                             if not res_partner:
    #                                 dict = {}
    #                                 if cust.get('PrimaryPhone'):
    #                                     dict['phone'] = cust.get('PrimaryPhone').get('FreeFormNumber')
    #                                 if cust.get('PrimaryEmailAddr'):
    #                                     dict['email'] = cust.get('PrimaryEmailAddr').get('Address', ' ')
    #                                 if cust.get('GivenName') and cust.get('FamilyName',' '):
    #                                     dict['name'] = cust.get('GivenName')+" "+cust.get('FamilyName',' ')
    #                                 if cust.get('GivenName') and not cust.get('FamilyName'):
    #                                     dict['name'] = cust.get('GivenName')
    #                                 if cust.get('FamilyName') and not cust.get('GivenName'):
    #                                     dict['name'] = cust.get('FamilyName')
    #                                 if not cust.get('FamilyName') and not cust.get('GivenName'):
    #                                     if cust.get('CompanyName'):
    #                                         dict['name'] = cust.get('CompanyName')
    #                                         print "Came here"
    #
    #         #                             if cust.get('Active'):
    #         #                                 if str(cust.get('Active')) == 'true':
    #         #                                     dict['active']=True
    #         #                                 else:
    #         #                                     dict['active']=False
    #                                 if cust.get('ParentRef'):
    #                                     print "GOT PARENT REF",cust.get('ParentRef')
    #                                     result = self.createOdooParentId(cust.get('ParentRef').get('value'))
    #                                     if result:
    #                                         dict['parent_id'] = result
    #                                         print "ATTACHED PARENT ID"
    #
    #                                 if cust.get('Id'):
    #                                     dict['x_quickbooks_id'] = cust.get('Id')
    #                                 if cust.get('Notes'):
    #                                     dict['comment'] = cust.get('Notes')
    #                                 if cust.get('BillWithParent'):
    #                                     dict['company_type'] = 'company'
    #                                 if cust.get('Mobile'):
    #                                     dict['mobile'] = cust.get('Mobile').get('FreeFormNumber')
    #                                 if cust.get('Fax'):
    #                                     dict['fax'] = cust.get('Fax').get('FreeFormNumber')
    #                                 if cust.get('WebAddr'):
    #                                     dict['website'] = cust.get('WebAddr').get('URI')
    #                                 if cust.get('Title'):
    #
    #                                     ''' If Title is present then first check in odoo if title exists or not
    #                                     if exists attach Id of tile else create new and attach its ID'''
    #                                     dict['title'] = self.attachCustomerTitle(cust.get('Title'))
    #         #                                 print "FINAL DICT TITLE IS :",dict['name'],dict['title']
    #         #                                 aaaaaaaaaa
    #                                 print "DICT TO ENTER IS : {}".format(dict)
    #                                 create = res_partner.create(dict)
    #                                 if create:
    #                                     recs.append(create.id)
    #                                     if not cust.get('ParentRef'):
    #                                         if cust.get('BillAddr'):
    #                                             ''' Getting BillAddr from quickbooks and Checking
    #                                                 in odoo to get countryId, stateId and create
    #                                                 state if not exists in odoo
    #                                                 '''
    #                                             dict = {}
    #                                             '''
    #                                             Get state id if exists else create new state and return it
    #                                             '''
    #                                             if cust.get('BillAddr').get('CountrySubDivisionCode'):
    #                                                 state_id = self.attachCustomerState(cust.get('BillAddr').get('CountrySubDivisionCode'),cust.get('BillAddr').get('Country'))
    #                                                 if state_id:
    #                                                     dict['state_id'] = state_id
    #                                                 print "STATE ID IS ::::::::::",state_id
    #
    #                                             country_id = self.env['res.country'].search([
    #                                                                                     ('name','=',cust.get('BillAddr').get('Country'))],limit=1)
    #                                             if country_id:
    #                                                 dict['country_id'] = country_id.id
    #                                             dict['parent_id'] = create.id
    #                                             dict['type'] = 'invoice'
    #                                             dict['zip'] = cust.get('BillAddr').get('PostalCode',' ')
    #                                             dict['city'] = cust.get('BillAddr').get('City')
    #                                             dict['street'] = cust.get('BillAddr').get('Line1')
    #                                             print "DICT IS ",dict
    #                                             child_create = res_partner.create(dict)
    #                                             if child_create:
    #                                                 print "Child Created BillAddr"
    #
    #                                         if cust.get('ShipAddr'):
    #                                             ''' Getting BillAddr from quickbooks and Checking
    #                                                 in odoo to get countryId, stateId and create
    #                                                 state if not exists in odoo
    #                                                 '''
    #                                             dict = {}
    #                                             if cust.get('ShipAddr').get('CountrySubDivisionCode'):
    #                                                 state_id = self.attachCustomerState(cust.get('ShipAddr').get('CountrySubDivisionCode'),cust.get('ShipAddr').get('Country'))
    #                                                 if state_id:
    #                                                     dict['state_id'] = state_id
    #                                                 print "STATE ID IS ::::::::::",state_id
    #
    #
    #                                             country_id = self.env['res.country'].search([('name','=',cust.get('ShipAddr').get('Country'))])
    #                                             if country_id:
    #                                                 dict['country_id'] = country_id[0].id
    #                                             dict['parent_id'] = create.id
    #                                             dict['type'] = 'delivery'
    #                                             dict['zip'] = cust.get('ShipAddr').get('PostalCode',' ')
    #                                             dict['city'] = cust.get('ShipAddr').get('City')
    #                                             dict['street'] = cust.get('ShipAddr').get('Line1')
    #                                             print "DICT IS ",dict
    #                                             child_create = res_partner.create(dict)
    #                                             if child_create:
    #                                                 print "Child Created ShipAddr"
    #                                     print "Created Res partner"
    #                                     self.x_quickbooks_last_customer_sync = fields.Datetime.now()
    #                                     if recs:
    #                                         self.x_quickbooks_last_customer_imported_id = max(recs)
    #                                 else:
    #                                     dict = {}
    #                                     if cust.get('PrimayPhone'):
    #                                         dict['phone'] = cust.get('PrimaryPhone').get('FreeFormNumber',' ')
    #
    #                                     if cust.get('PrimaryEmailAddr'):
    #                                         dict['email'] = cust.get('PrimaryEmailAddr').get('Address', ' ')
    #                                     write = res_partner.write(dict)
    #                                     if write :
    #                                         print "Written Successfully"
    #             else:
    #                 print "Didnt got Data"

    # ----------------------------------------------------------------------------------------------------------

    # function called when clicked on sync employee button
    # @api.multi
    def import_employee(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + company.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'

            '''ALL EMPLOYEES WITH ALL THE INFO'''
            query = "select * from employee WHERE Id > '%s' order by Id" % (company.quickbooks_last_employee_imported_id)

            data = requests.request('GET', company.url + str(company.realm_id) + "/query?query=" + query,
                                    headers=headers)
            if data:
                recs = []
                parsed_data = json.loads(str(data.text))
                if parsed_data:
                    _logger.info("Employee data  is ------------------->{}".format(parsed_data))

                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Employee'):

                        for emp in parsed_data.get('QueryResponse').get('Employee'):

                            # ''' This will avoid duplications'''

                            hr_employee = self.env['hr.employee'].search([('quickbook_id', '=', emp.get('Id'))])

                            dict_e = {}

                            if emp.get('DisplayName'):
                                dict_e['name'] = emp.get('DisplayName')

                            if emp.get('PrimaryPhone'):
                                dict_e['mobile_phone'] = emp.get('PrimaryPhone').get('FreeFormNumber')

                            if emp.get('PrimaryEmailAddr'):
                                dict_e['work_email'] = emp.get('PrimaryEmailAddr').get('Address', ' ')

                            if emp.get('Id'):
                                dict_e['quickbook_id'] = emp.get('Id')

                            if emp.get('Mobile'):
                                dict_e['work_phone'] = emp.get('Mobile').get('FreeFormNumber')

                            if emp.get('EmployeeNumber'):
                                dict_e['employee_no'] = emp.get('EmployeeNumber')

                            if emp.get('BirthDate'):
                                dict_e['birthday'] = emp.get('BirthDate')

                            if emp.get('Gender'):
                                if emp.get('Gender') == 'Female':
                                    dict_e['gender'] = 'female'
                                if emp.get('Gender') == 'Male':
                                    dict_e['gender'] = 'male'
                                if emp.get('Gender') == 'Other':
                                    dict_e['gender'] = 'other'

                            # if emp.get('GivenName') and emp.get('FamilyName', ' '):
                            #     dict_e['name'] = emp.get('GivenName') + " " + emp.get('FamilyName', ' ')
                            #
                            # if emp.get('GivenName') and not emp.get('FamilyName'):
                            #     dict_e['name'] = emp.get('GivenName')

                            if emp.get('Notes'):
                                dict_e['notes'] = emp.get('Notes')

                            if emp.get('HiredDate'):
                                dict_e['hired_date'] = emp.get('HiredDate')

                            if emp.get('ReleasedDate'):
                                dict_e['released_date'] = emp.get('ReleasedDate')

                            if emp.get('BillRate'):
                                dict_e['billing_rate'] = emp.get('BillRate')

                            if emp.get('SSN'):
                                dict_e['ssn'] = emp.get('SSN')

                            if not hr_employee:

                                '''If employee is not present we create it'''

                                employee_create = hr_employee.create(dict_e)

                                if employee_create:
                                    _logger.info('Employee Created Sucessfully..!!')

                                    recs.append(employee_create.id)
                                    if emp.get('PrimaryAddr'):

                                        dict_c = {}

                                        if emp.get('PrimaryAddr').get('CountrySubDivisionCode'):

                                            state_id = self.State(
                                                emp.get('PrimaryAddr').get('CountrySubDivisionCode'),
                                                emp.get('PrimaryAddr').get('Country'))
                                            if state_id:
                                                dict_c['state_id'] = state_id
                                        country_id = self.env['res.country'].search([
                                            ('code', '=', emp.get('PrimaryAddr').get('CountrySubDivisionCode'))],
                                            limit=1)
                                        if country_id:
                                            dict_c['country_id'] = country_id.id
                                        if emp.get('DisplayName'):
                                            dict_c['name'] = emp.get('DisplayName')
                                        if emp.get('PrimaryAddr').get('Id'):
                                            dict_c['qbo_customer_id'] = emp.get('PrimaryAddr').get('Id')

                                        if emp.get('PrimaryAddr').get('PostalCode', ' '):
                                            dict_c['zip'] = emp.get('PrimaryAddr').get('PostalCode', ' ')
                                        if emp.get('PrimaryAddr').get('City'):
                                            dict_c['city'] = emp.get('PrimaryAddr').get('City')

                                        if emp.get('PrimaryAddr').get('Line1'):
                                            dict_c['street'] = emp.get('PrimaryAddr').get('Line1')

                                        if emp.get('PrimaryAddr'):
                                            check_id = emp.get('PrimaryAddr').get('Id')

                                            cust_obj = self.env['res.partner'].search([['qbo_customer_id', 'ilike', check_id]])

                                            if cust_obj:
                                                for cust_id in cust_obj:
                                                    cust_id.write(dict_c)
                                                    '''CREATING NEW EMP'S EXISTING ADDRESS'''

                                                    employee_obj = self.env['hr.employee'].search(
                                                        [['quickbook_id', '=', emp.get('Id')]])
                                                    _logger.info("Employee object is --------------------> {}".format(employee_obj))
                                                    if employee_obj:
    #                                                     for check in employee_obj:
                                                            res = employee_obj.update({

                                                                'address_id': cust_id.id
                                                            })
                                            else:
                                                '''CREATING NEW EMP'S NEW ADDRESS'''

                                                address_create = self.env['res.partner'].create(dict_c)
#                                                 for addr_create in address_create:
                                                dict_c['address_id'] = address_create.id

                                                # write = employee_create.write(dict_c)
                                                # if write:
                                                #     print("Employee Created Successfully")

                                        # self.quickbooks_last_employee_sync = fields.Datetime.now()
                                        company.quickbooks_last_employee_imported_id = int(emp.get('Id'))

                                        # write = employee_create.write(dict_c)
                                        # if write:
                                        #     print("Employee Created Successfully")

                            else:
                                if emp.get('PrimaryAddr'):
                                    dict_c = {}

                                    if emp.get('PrimaryAddr').get('CountrySubDivisionCode'):

                                        state_id = self.State(
                                            emp.get('PrimaryAddr').get('CountrySubDivisionCode'),
                                            emp.get('PrimaryAddr').get('Country'))
                                        if state_id:
                                            dict_c['state_id'] = state_id
                                    country_id = self.env['res.country'].search([
                                        ('code', '=', emp.get('PrimaryAddr').get('CountrySubDivisionCode'))],
                                        limit=1)
                                    if country_id:
                                        dict_c['country_id'] = country_id.id
                                    # dict['parent_id'] = create.id

                                    if emp.get('DisplayName'):
                                        dict_c['name'] = emp.get('DisplayName')
                                    if emp.get('PrimaryAddr').get('Id'):
                                        dict_c['qbo_customer_id'] = emp.get('PrimaryAddr').get('Id')
                                    if emp.get('PrimaryAddr').get('PostalCode', ' '):
                                        dict_c['zip'] = emp.get('PrimaryAddr').get('PostalCode', ' ')
                                    if emp.get('PrimaryAddr').get('City'):
                                        dict_c['city'] = emp.get('PrimaryAddr').get('City')

                                    if emp.get('PrimaryAddr').get('Line1'):
                                        dict_c['street'] = emp.get('PrimaryAddr').get('Line1')

                                '''If employee is present we update it'''
                                employee_write = hr_employee.write(dict_e)

                                if emp.get('PrimaryAddr'):
                                    check_id = emp.get('PrimaryAddr').get('Id')
                                    cust_obj = self.env['res.partner'].search([['qbo_customer_id', '=', check_id]])

                                    if cust_obj:

                                        '''UPDATING EXISTING EMP'S EXISTING ADDRESS'''

                                        cust_obj.write(dict_c)
                                        employee_obj = self.env['hr.employee'].search(
                                            [['quickbook_id', '=', emp.get('Id')]])
                                        if employee_obj:
                                            res = employee_obj.update({

                                                'address_id': cust_obj.id
                                            })

                                    else:
                                        '''UPDATING EXISTING EMP'S NEW ADDRESS'''

                                        address = self.env['res.partner'].create(dict_c)
                                        dict_c['address_id'] = address.id

                                        employee_obj = self.env['hr.employee'].search([['quickbook_id', '=', emp.get('Id')]])
                                        if employee_obj:
                                            res = employee_obj.update({

                                                'address_id': address.id
                                            })

                                if employee_write:
                                    company.quickbooks_last_employee_imported_id = int(emp.get('Id'))
                                    _logger.info('Employee Updated Successfully :: %s', emp.get('Id'))

            else:
                _logger.warning(_('Empty data'))

    def State(self, state, country):

        state_id = False
        if state and country:
            country_id = self.env['res.country'].search([('name', '=', country)], limit=1)
            if country_id:

                state_id = self.env['res.country.state'].search([('name', '=', state)], limit=1)

                if state_id and state_id.country_id.id == country_id.id:
                    return state_id.id
                else:
                    new_state_id = self.env['res.country.state'].create({
                        'country_id': country_id.id,
                        'code': state[:2],
                        'name': state
                    })
                    if new_state_id:
                        return new_state_id.id

    # -------------------------------------DEPARTMENT-----------------------------------------

    # function called when clicked on sync dept button
    # @api.multi
    def import_department(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + company.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'

            query = "select * from department WHERE Id > '%s' order by Id" % (company.quickbooks_last_dept_imported_id)
            data = requests.request('GET', company.url + str(company.realm_id) + "/query?query=" + query,
                                    headers=headers)

            if data:
                recs = []
                parsed_data = json.loads(str(data.text))
                if parsed_data:
                    _logger.info("Department data  is ------------------->{}".format(parsed_data))
                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Department'):

                        for emp in parsed_data.get('QueryResponse').get('Department'):

                            # ''' This will avoid duplications'''

                            hr_dept = self.env['hr.department'].search([('quickbook_id', '=', emp.get('Id'))])
                            dict_e = {}

                            if emp.get('Name'):
                                dict_e['name'] = emp.get('Name')

                            if emp.get('Id'):
                                dict_e['quickbook_id'] = emp.get('Id')

                            if emp.get('ParentRef'):
                                if emp.get('ParentRef').get('value'):
                                    parent_id = self.env['hr.department'].search([('quickbook_id', '=', emp.get('ParentRef').get('value'))])
                                    dict_e['parent_id'] = parent_id.id

                            if not hr_dept:

                                '''If employee is not present we create it'''

                                dept_create = hr_dept.create(dict_e)
                                if dept_create:

                                    company.quickbooks_last_dept_imported_id = int(emp.get('Id'))
                                    _logger.info('Department Created Sucessfully..!!')
                                else:
                                    _logger.info('Department Not Created Sucessfully..!!')
                            else:
                                dept_write = hr_dept.write(dict_e)
                                if dept_write:
                                    company.quickbooks_last_dept_imported_id = int(emp.get('Id'))
                                    _logger.info('Department Updated Sucessfully..!!')
                                else:
                                    _logger.info('Department Not Updated Sucessfully..!!')
            else:
                _logger.warning(_('Empty data'))

    # ---------------------------------SALE ORDER------------------------------------------------------

    # @api.multi
    def import_sale_order(self):
        _logger.info("Sale order")
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        _logger.info("Company is-> {}".format(company))
        if company.access_token:
            _logger.info("Access token is ---> {}".format(company.access_token))
            headers = {}
            headers['Authorization'] = 'Bearer ' + company.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'

            query = "select * from estimate WHERE Id > '%s' order by Id  STARTPOSITION %s MAXRESULTS %s " % (company.quickbooks_last_sale_imported_id, company.start, company.limit)
            _logger.info("Query is -----> {}".format(query))
            data = requests.request('GET', company.url + str(company.realm_id) + "/query?query=" + query,
                                    headers=headers)
            _logger.info("************data{}".format(data.text))
            if data:
                recs = []

                parsed_data = json.loads(str(data.text))
                if parsed_data:

                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Estimate'):

                        for cust in parsed_data.get('QueryResponse').get('Estimate'):
                            if "CustomerRef"  in cust and cust.get('CustomerRef').get('value'):
                            # searching sales order
                                sale_order = self.env['sale.order'].search(
                                    [('quickbook_id', '=', cust.get('Id'))])
                                _logger.info("Sale order exists or not!!!!!---->{}".format(sale_order))
                                if not sale_order:
                                    _logger.info("Creating Sales order...")
                                    _logger.info("Partner value is ---------------> {}".format(cust.get('CustomerRef').get('value')))
                                    res_partner = self.env['res.partner'].search(
                                        [('qbo_customer_id', '=', cust.get('CustomerRef').get('value')), ('type', '=', 'contact')], limit=1)
                                    _logger.info("RES PARTNER IS -> {}".format(res_partner))
                                    if res_partner:
                                        dict_s = {}

                                        if cust.get('Id'):
                                            dict_s['partner_id'] = res_partner.id
                                            dict_s['state'] = 'sale'
                                            dict_s['quickbook_id'] = cust.get('Id')

                                        if cust.get('DocNumber'):
                                            dict_s['name'] = cust.get('DocNumber')

                                        if cust.get('PaymentRefNum'):
                                            dict_s['client_order_ref'] = cust.get('PaymentRefNum')

                                        if cust.get('TotalAmt'):
                                            dict_s['amount_total'] = cust.get('TotalAmt')

                                        ele_in_list = len(cust.get('Line'))
                                        dict_t = cust.get('Line')[ele_in_list - 1]
                                        _logger.info("Dictionary before creating is----> {}".format(dict_t))
#                                         if 'DiscountLineDetail' in dict_t and dict_t.get('DiscountLineDetail'):
#                                             dict_s['check'] = True
#                                             _logger.info("inside dictionary of discount")
#                                             if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                                 dict_s['discount_type'] = 'percentage'
#                                                 print("perc is ***********",'percentage')
#                                                 dict_s['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                                 print("amount is :", dict_t.get('DiscountLineDetail').get('DiscountPercent'))
#                                                 dict_s['percentage_amt'] = dict_t.get('Amount')
#                                                 print("perc amt is **************",dict_t.get('Amount'))
#                                             else:
#                                                 dict_s['discount_type'] = 'value'
#                                                 print("disc type:",'value')
#                                                 dict_s['amount'] = dict_t.get('Amount')
#                                                 print("amount is ***********",dict_t.get('Amount'))

                                        now = datetime.now()
                                        dict_s['date_order'] = now.strftime("%Y-%m-%d %H:%M:%S")
                                        _logger.info("Dictionary is--->{}:".format(dict_s))
                                        so_obj = self.env['sale.order'].create(dict_s)

                                        if so_obj:
                                            self._cr.commit()
                                            _logger.info("WRITING QBO ID TO SALE ORDER {}".format(so_obj.id))
                                            so_obj.write({'quickbook_id' : cust.get('Id')})
                                            _logger.info("Object is --->{}".format(so_obj))
                                            _logger.info('Sale Order Created...!!! :: %s', cust.get('Id'))
                                        # ///////////////////////////////////////////////////////////////
                                        custom_tax_id = None
                                        for i in cust.get('Line'):
                                            _logger.info("Particular instance is ------------> {}".format(i))
                                            if  'TxnTaxDetail' in cust and cust.get('TxnTaxDetail'):
                                                if cust.get('TxnTaxDetail').get('TxnTaxCodeRef'):
                                                    _logger.info("Transaction data!!!")
                                                    if cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value'):

                                                        qb_tax_id = cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value')
                                                        record = self.env['account.tax']
                                                        tax = record.search([('qbo_tax_id', '=', qb_tax_id)])

                                                        if tax:
                                                            custom_tax_id = [(6, 0, [tax.id])]
                                                        else:
                                                            custom_tax_id = None

                                            if 'SalesItemLineDetail' in i and i.get('SalesItemLineDetail'):
                                                _logger.info("SalesItem Data")
                                                res_product = self.env['product.product'].search(
                                                    [('qbo_product_id', '=', i.get('SalesItemLineDetail').get('ItemRef').get('value'))])

                                                if res_product:
                                                    dict_l = {}

                                                    if i.get('Id'):
                                                        dict_l['qb_id'] = int(i.get('Id'))

                                                    if i.get('SalesItemLineDetail').get('TaxCodeRef'):
                                                        tax_val = i.get('SalesItemLineDetail').get('TaxCodeRef').get(
                                                            'value')
                                                        if tax_val == 'TAX':

                                                            dict_l['tax_id'] = custom_tax_id
                                                        # else:
                                                        #     dict_l['tax_id'] =

                                                    dict_l['order_id'] = so_obj.id

                                                    dict_l['product_id'] = res_product.id

                                                    if i.get('SalesItemLineDetail').get('Qty'):
                                                        dict_l['product_uom_qty'] = i.get('SalesItemLineDetail').get('Qty')
                                                    else:
                                                        dict_l['product_uom_qty'] = 0.0

                                                    if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                        dict_l['price_unit'] = i.get('SalesItemLineDetail').get('UnitPrice')
                                                    else:
                                                        dict_l['price_unit'] = 0.0

                                                    if i.get('Description'):
                                                        dict_l['name'] = i.get('Description')
                                                    else:
                                                        dict_l['name'] = 'NA'
                                                    _logger.info("Dictionary for sale order line is --------> {}".format(dict_l))
                                                    create_p = self.env['sale.order.line'].create(dict_l)
                                                    self._cr.commit()
                                                    _logger.info("Sale order line --------------->{}".format(create_p))
                                                    if create_p:
                                                        company.quickbooks_last_sale_imported_id = int(cust.get('Id'))

                                else:
                                    _logger.info("Else part------")
                                    res_partner = self.env['res.partner'].search(
                                        [('qbo_customer_id', '=', cust.get('CustomerRef').get('value'))])
                                    _logger.info("Directing to else part....->{}".format(res_partner))
                                    if res_partner:
                                        dict_s = {}

                                        if cust.get('Id'):
                                            dict_s['partner_id'] = res_partner.id
                                            dict_s['quickbook_id'] = cust.get('Id')
                                            dict_s['state'] = 'sale'

                                        now = datetime.now()
                                        dict_s['date_order'] = now.strftime("%Y-%m-%d %H:%M:%S")

                                        if cust.get('PaymentRefNum'):
                                            dict_s['client_order_ref'] = cust.get('PaymentRefNum')

                                        if cust.get('DocNumber'):
                                            dict_s['name'] = cust.get('DocNumber')

                                        if cust.get('TotalAmt'):
                                            dict_s['amount_total'] = cust.get('TotalAmt')

                                        ele_in_list = len(cust.get('Line'))

                                        dict_t = cust.get('Line')[ele_in_list - 1]
#                                         if dict_t.get('DiscountLineDetail'):
#                                             dict_s['check'] = True
#
#                                             if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                                 dict_s['discount_type'] = 'percentage'
#                                                 dict_s['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                                 dict_s['percentage_amt'] = dict_t.get('Amount')
#                                             else:
#                                                 dict_s['discount_type'] = 'value'
#                                                 dict_s['amount'] = dict_t.get('Amount')
                                        _logger.info("Dict for update is ----> {}".format(dict_s))
                                        update_so = sale_order.write(dict_s)
                                        _logger.info("update obj {}".format(update_so))
                                        if update_so:
                                            _logger.info('Sale Order Updated...!!! :: %s', cust.get('Id'))
                                        custom_tax_id = None
                                        # discount_amt = 0
                                        for i in cust.get('Line'):
                                            if 'TxnTaxDetail' in cust and  cust.get('TxnTaxDetail'):
                                                if cust.get('TxnTaxDetail').get('TxnTaxCodeRef'):

                                                    if cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value'):
                                                        qb_tax_id = cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value')
                                                        record = self.env['account.tax']
                                                        tax = record.search([('qbo_tax_id', '=', qb_tax_id)])
                                                        if tax:
                                                            custom_tax_id = [(6, 0, [tax.id])]
                                                        else:
                                                            custom_tax_id = None

                                            if 'SalesItemLineDetail' in i and i.get('SalesItemLineDetail'):
                                                res_product = self.env['product.product'].search(
                                                    [('qbo_product_id', '=', i.get('SalesItemLineDetail').get('ItemRef').get('value'))])
                                                if res_product:
                                                    s_order_line = self.env['sale.order.line'].search(
                                                        ['&', ('product_id', '=', res_product.id),
                                                         (('order_id', '=', sale_order.id))])

                                                    if s_order_line:

                                                        dict_lp = {}

                                                        if i.get('SalesItemLineDetail').get('Qty'):
                                                            quantity = i.get('SalesItemLineDetail').get(
                                                                'Qty')
                                                        else:
                                                            quantity = 0

                                                        if i.get('SalesItemLineDetail').get('TaxCodeRef'):

                                                            # print("TAX AVAILABLE : ",
                                                            #       i.get('SalesItemLineDetail').get('TaxCodeRef').get(
                                                            #           'value'))
                                                            tax_val = i.get('SalesItemLineDetail').get('TaxCodeRef').get(
                                                                'value')
                                                            if tax_val == 'TAX':
                                                                # custom_tax_id = [(6, 0, [tax.id])]
                                                                custom_tax_id_id = custom_tax_id
                                                            else:
                                                                custom_tax_id_id = None

                                                        if i.get('Id'):
                                                            ol_qb_id = int(i.get('Id'))
                                                        else:
                                                            ol_qb_id = 0

                                                        if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                            sp = i.get('SalesItemLineDetail').get(
                                                                'UnitPrice')
                                                        else:
                                                            sp = 0

                                                        if i.get('Description'):
                                                            description = i.get('Description')
                                                        else:
                                                            description = 'NA'

                                                        create_po = self.env['sale.order.line'].search(
                                                            ['&', ('product_id', '=', res_product.id),
                                                             (('order_id', '=', sale_order.id))])

                                                        if create_po:
                                                            res = create_po.update({

                                                                'product_id': res_product.id,
                                                                'name': description,
                                                                'product_uom_qty': quantity,
                                                                'tax_id': custom_tax_id_id,
                                                                'qb_id': ol_qb_id,
                                                                # 'product_uom': 1,
                                                                'price_unit': sp,
                                                            })

                                                        if create_po:
                                                            company.quickbooks_last_sale_imported_id = int(cust.get('Id'))

                                                    else:
                                                        '''CODE FOR NEW LINE IN EXISTING SALE ORDER'''
                                                        _logger.info("Code for new line in existing sale order")
                                                        res_product = self.env['product.product'].search(
                                                            [('qbo_product_id', '=', i.get('SalesItemLineDetail').get('ItemRef').get('value'))])

                                                        if res_product:
                                                            dict_l = {}
                                                            if i.get('Id'):
                                                                dict_l['qb_id'] = int(i.get('Id'))

                                                            # if discount_amt > 0:
                                                            #     dict_l['discount'] = discount_amt

                                                            if i.get('SalesItemLineDetail').get('TaxCodeRef'):

                                                                # print("TAX AVAILABLE : ",
                                                                #       i.get('SalesItemLineDetail').get('TaxCodeRef').get(
                                                                #           'value'))
                                                                tax_val = i.get('SalesItemLineDetail').get(
                                                                    'TaxCodeRef').get(
                                                                    'value')
                                                                if tax_val == 'TAX':

                                                                    dict_l['tax_id'] = custom_tax_id
                                                                else:
                                                                    dict_l['tax_id'] = None

                                                            dict_l['order_id'] = sale_order.id
                                                            # dict_l['order_id'] = sale_order.id

                                                            dict_l['product_id'] = res_product.id

                                                            if i.get('SalesItemLineDetail').get('Qty'):
                                                                dict_l['product_uom_qty'] = i.get(
                                                                    'SalesItemLineDetail').get('Qty')
                                                                # cust.get('Line')[0].get('SalesItemLineDetail').get('Qty')
                                                            else:
                                                                dict_l['product_uom_qty'] = 0

                                                            if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                                dict_l['price_unit'] = i.get(
                                                                    'SalesItemLineDetail').get('UnitPrice')
                                                            else:
                                                                dict_l['price_unit'] = 0

                                                            if i.get('Description'):
                                                                dict_l['name'] = i.get('Description')
                                                            else:
                                                                dict_l['name'] = 'NA'

                                                            # dict_l['product_uom'] = 1
                                                            _logger.info("Sale order line of update is ----> {}".format(dict_l))
                                                            create_p = self.env['sale.order.line'].create(dict_l)
                                                            _logger.info("Sale order line of creation is {}".format(create_p))
                                                            if create_p:
                                                                company.quickbooks_last_sale_imported_id = int(cust.get('Id'))
            else:
                _logger.warning(_('Empty data'))

    # --------------------------------- INVOICE  -----------------------------------------------
    @api.model
    def check_if_lines_present(self, cust):
        if cust.get('Line'):
            for i in cust.get('Line'):
                if i.get('SalesItemLineDetail'):
                    return True
                else:
                    return False
        else:
            return False

    # @api.model
    # def check_if_lines_present_vendor_bill(self, cust):
    #     if 'Line' in cust and cust.get('Line'):
    #         for i in cust.get('Line'):
    #             if i.get('ItemBasedExpenseLineDetail'):
    #                 _logger.info("ItemBasedExpenseLineDetail-----------------> {}".format(i.get('ItemBasedExpenseLineDetail')))
    #                 return True
    #             else:
    #                 _logger.info("NO ItemBasedExpenseLineDetail ")
    #                 return False
    #     else:
    #         return False

    # -------------------------------------------- PURCHASE  ORDER  -------------------------------------------------

    # @api.multi
    def import_purchase_order(self):
        _logger.info("inside purchase order *********************")
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + company.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'
            query = "select * from purchaseorder WHERE Id > '%s' order by Id" % (company.quickbooks_last_purchase_imported_id)
            data = requests.request('GET', company.url + str(company.realm_id) + "/query?query=" + query,
                                    headers=headers)
            if data:

                recs = []
                parsed_data = json.loads(str(data.text))
                if parsed_data:

                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('PurchaseOrder'):
                        for cust in parsed_data.get('QueryResponse').get('PurchaseOrder'):

                            purchase_order = self.env['purchase.order'].search([('quickbook_id', '=', cust.get('Id'))])

                            if not purchase_order:
                                res_partner = self.env['res.partner'].search([('qbo_vendor_id', '=', cust.get('VendorRef').get('value'))], limit=1)

                                if res_partner:
                                    dict_s = {}

                                    if cust.get('Id'):
                                        dict_s['partner_id'] = res_partner.id
                                        dict_s['quickbook_id'] = cust.get('Id')
                                    else:
                                        dict_s['parent_id'] = cust.get('VendorRef').get('name')

                                    if cust.get('POStatus'):
                                        dict_s['state'] = 'purchase'

                                    if cust.get('DocNumber'):
                                        dict_s['name'] = cust.get('DocNumber')

                                    so_obj = self.env['purchase.order'].create(dict_s)
                                    if so_obj:
                                        _logger.info('PO Created Successfully :: %s', so_obj)

                                    for i in cust.get('Line'):
                                        if i.get('ItemBasedExpenseLineDetail'):
                                            res_product = self.env['product.product'].search(
                                                [('qbo_product_id', '=', i.get('ItemBasedExpenseLineDetail').get('ItemRef').get('value'))])

                                            if res_product:
                                                dict_l = {}

                                                dict_l.clear()
                                                dict_l['order_id'] = so_obj.id
                                                dict_l['product_id'] = res_product.id

                                                if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                    dict_l['product_qty'] = i.get('ItemBasedExpenseLineDetail').get('Qty')

                                                if i.get('Id'):
                                                    dict_l['qb_id'] = int(i.get('Id'))
                                                    dict_l['date_planned'] = so_obj.date_order

                                                dict_l['product_uom'] = 1

                                                if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                    dict_l['price_unit'] = i.get('ItemBasedExpenseLineDetail').get('UnitPrice')
                                                else:
                                                    dict_l['price_unit'] = 0.0

                                                if i.get('Description'):
                                                    dict_l['name'] = i.get('Description')
                                                else:
                                                    dict_l['name'] = 'NA'

                                                create_p = self.env['purchase.order.line'].create(dict_l)
                                                if create_p:
                                                    company.quickbooks_last_purchase_imported_id = cust.get('Id')

                            else:

                                res_partner = self.env['res.partner'].search(
                                    [('qbo_vendor_id', '=', cust.get('VendorRef').get('value'))])

                                if res_partner:

                                    dict_s = {}

                                    if cust.get('Id'):
                                        dict_s['partner_id'] = res_partner.id
                                        dict_s['quickbook_id'] = cust.get('Id')
                                        # dict_s['purchase_order_id'] = cust.get('DocNumber')
                                        # dict_s['state'] = 'purchase'
                                    else:
                                        dict_s['parent_id'] = cust.get('VendorRef').get('name')

                                    if cust.get('POStatus'):
                                        # if cust.get('POStatus') == 'Open':
                                        #     dict_s['state'] = 'draft'
                                        # if cust.get('POStatus') == 'Closed':
                                        dict_s['state'] = 'purchase'
                                    if cust.get('DocNumber'):
                                        dict_s['name'] = cust.get('DocNumber')

                                    purchase_order.write(dict_s)
                                    _logger.info('PO Updated Successfully..!!')

                                    for i in cust.get('Line'):

                                        if i.get('ItemBasedExpenseLineDetail'):

                                            res_product = self.env['product.product'].search(
                                                [('qbo_product_id', '=', i.get('ItemBasedExpenseLineDetail').get('ItemRef').get(
                                                    'value'))])
                                            if res_product:
                                                p_order_line = self.env['purchase.order.line'].search(
                                                    ['&', ('product_id', '=', res_product.id),
                                                     (('order_id', '=', purchase_order.id))], limit=1)

                                                if p_order_line:

                                                    dict_lp = {}

                                                    if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                        quantity = i.get('ItemBasedExpenseLineDetail').get('Qty')

                                                    if i.get('Id'):
                                                        ol_qb_id = int(i.get('Id'))

                                                    if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                        sp = i.get('ItemBasedExpenseLineDetail').get('UnitPrice')
                                                    else:
                                                        sp = 0.0

                                                    if i.get('Description'):
                                                        description = i.get('Description')
                                                    else:
                                                        description = 'NA'

                                                    create_po = self.env['purchase.order.line'].search(
                                                        ['&', ('product_id', '=', res_product.id), (('order_id', '=', purchase_order.id))])
                                                    if create_po:
                                                        res = create_po.update({

                                                            'product_id': res_product.id,
                                                            'name': description,
                                                            'product_qty': quantity,
                                                            'date_planned': p_order_line.date_order,
                                                            'qb_id': ol_qb_id,
                                                            'product_uom': 1,
                                                            'price_unit': sp,
                                                        })

                                                    if create_po:
                                                        company.quickbooks_last_purchase_imported_id = cust.get('Id')

                                                else:
                                                    '''CREATE NEW PURCHSE ORDER LINES IN EXISTING PURCHASE ORDER'''

                                                    dict_l = {}
                                                    dict_l.clear()
                                                    dict_l['order_id'] = purchase_order.id
                                                    dict_l['product_id'] = res_product.id

                                                    if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                        dict_l['product_qty'] = i.get('ItemBasedExpenseLineDetail').get('Qty')

                                                    if i.get('Id'):
                                                        dict_l['qb_id'] = int(i.get('Id'))
                                                        dict_l['date_planned'] = purchase_order.date_order

                                                    dict_l['product_uom'] = 1

                                                    if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                        dict_l['price_unit'] = i.get('ItemBasedExpenseLineDetail').get('UnitPrice')
                                                    else:
                                                        dict_l['price_unit'] = 0.0

                                                    if i.get('Description'):
                                                        dict_l['name'] = i.get('Description')
                                                    else:
                                                        dict_l['name'] = 'NA'

                                                    create_p = self.env['purchase.order.line'].create(dict_l)
                                                    if create_p:
                                                        company.quickbooks_last_purchase_imported_id = cust.get('Id')

            else:
                _logger.warning(_('Empty data'))

    # ---------------------------------VENDOR BILLS------------------------------------------------------

    # @api.multi
    def import_vendor_bill_1(self):
        _logger.info("inside vendor bill ****************************")
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + self.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'

            query = "select * from bill WHERE Id > '%s' order by Id" % (
                company.quickbooks_last_vendor_bill_imported_id)

            data = requests.request('GET', self.url + str(self.realm_id) + "/query?query=" + query,
                                    headers=headers)
            if data:
                _logger.info("Vendor bill data is -------------------->{}".format(data.text))
                recs = []
                parsed_data = json.loads(str(data.text))
                if parsed_data:
                    _logger.info("Parsed data for vendor bill is -------------> {}".format(parsed_data))
                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('Bill'):

                        for cust in parsed_data.get('QueryResponse').get('Bill'):
                            # searching sales order
                            line_present = self.check_if_lines_present_vendor_bill(cust)
                            _logger.info('ORDER LINES NOT PRESENT IN VENDOR BILL :: %s', line_present)
                            if not line_present:
                                continue

                            bill = self.env['account.move'].search(
                                [('qbo_invoice_id', '=', cust.get('Id'))])
                            _logger.info("Bill search is --------------> {}".format(bill))
                            if not bill:

                                _logger.info("No bill.")
                                _logger.info("Vendor value is -----------------> {}".format(cust.get('VendorRef').get('value')))
                                res_partner = self.env['res.partner'].search(
                                    [('qbo_vendor_id', '=', cust.get('VendorRef').get('value'))])
                                _logger.info("Res partner is -------------------> {}".format(res_partner))
                                if res_partner:
                                    dict_i = {}
                                    if cust.get('Id'):
                                        dict_i['partner_id'] = res_partner.id

                                        dict_i['qbo_invoice_id'] = cust.get('Id')

                                        dict_i['company_id'] = self.id

                                        dict_i['type'] = 'in_invoice'

                                    if cust.get('CurrencyRef'):
                                        if cust.get('CurrencyRef').get('value'):
                                            currency = self.env['res.currency'].search(
                                                [('name', '=', cust.get('CurrencyRef').get('value'))], limit=1)
                                            dict_i['currency_id'] = currency.id

                                    if res_partner.customer_rank:
                                        sale = self.env['account.journal'].search([('type', 'in', ['sale','cash'])], limit=1)
                                        if sale:
                                            dict_i['journal_id'] = sale.id
                                            _logger.info("Journal was attached..")
                                        else:
                                            _logger.info("No Journal was found..")
                                    if res_partner.supplier_rank:
                                        purchase = self.env['account.journal'].search([('type', 'in', ['purchase','cash'])],
                                                                                      limit=1)
                                        if purchase:
                                            dict_i['journal_id'] = purchase.id
                                            _logger.info("Journal attached..")
                                        else:
                                            _logger.info("No Journal was found...")

                                        # dict_i['journal_id'] = 1
                                        dict_i['reference_type'] = ''
                                    # if cust.get('DocNumber'):
                                    #     dict_i['number'] = cust.get('DocNumber')
                                    if cust.get('Balance'):
                                        dict_i['state'] = 'draft'
                                        # dict_i['residual'] = cust.get('Balance')
                                        # dict_i['residual_signed'] = cust.get('Balance')
                                        dict_i['amount_residual'] = cust.get('Balance')
                                        dict_i['amount_residual_signed'] = cust.get('Balance')
                                    else:
                                        dict_i['amount_residual'] = 0.0
                                        dict_i['amount_residual_signed'] = 0.0

                                    if cust.get('DueDate'):
                                        dict_i['invoice_date_due'] = cust.get('DueDate')
                                    if cust.get('TxnDate'):
                                        dict_i['invoice_date'] = cust.get('TxnDate')

                                    ele_in_list = len(cust.get('Line'))
                                    dict_t = cust.get('Line')[ele_in_list - 1]
#                                     if dict_t.get('DiscountLineDetail'):
#                                         dict_i['check'] = True
#
#                                         if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                             dict_i['discount_type'] = 'percentage'
#                                             dict_i['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                             dict_i['percentage_amt'] = dict_t.get('Amount')
#                                         else:
#                                             dict_i['discount_type'] = 'value'
#                                             dict_i['amount'] = dict_t.get('Amount')

                                    # if cust.get('TotalTax'):
                                    #     dict_i['amount_tax'] = cust.get('TotalTax')

                                    if cust.get('TotalAmt'):
                                        dict_i['amount_total'] = cust.get('TotalAmt')
                                    _logger.info("Dictionary for creation of vendor bill is ---> {}".format(dict_i))
                                    invoice_obj = self.env['account.move'].create(dict_i)
                                    _logger.info("Invoice object is --------> {}".format(invoice_obj))
                                    if invoice_obj:
                                        _logger.info('Vendor Bill Created Successfully :: %s', cust.get('Id'))

                                    custom_tax_id = None

                                    for i in cust.get('Line'):
                                        dict_ol = {}

                                        if i.get('ItemBasedExpenseLineDetail'):
                                            res_product = self.env['product.product'].search([('qbo_product_id', '=',
                                                                                               i.get(
                                                                                                   'ItemBasedExpenseLineDetail').get(
                                                                                                   'ItemRef').get(
                                                                                                   'value'))])
                                            if res_product:
                                                dict_ol.clear()
                                                dict_ol['move_id'] = invoice_obj.id
                                                dict_ol['product_id'] = res_product.id

                                                if i.get('Id'):
                                                    dict_ol['qb_id'] = int(i.get('Id'))
                                                    dict_ol['tax_ids'] = None

                                                if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                    dict_ol['quantity'] = i.get('ItemBasedExpenseLineDetail').get('Qty')

                                                if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                    dict_ol['price_unit'] = float(
                                                        i.get('ItemBasedExpenseLineDetail').get('UnitPrice'))
                                                else:
                                                    if not i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                        dict_ol['quantity'] = 1
                                                        dict_ol['price_unit'] = float(
                                                            i.get('Amount'))
                                                    else:
                                                        dict_ol['price_unit'] = 0.0

                                                if i.get('Description'):
                                                    dict_ol['name'] = i.get('Description')
                                                else:
                                                    dict_ol['name'] = 'NA'
                                                if res_product.property_account_expense_id:
                                                    dict_ol['account_id'] = res_product.property_account_expense_id.id
                                                else:
                                                    dict_ol['account_id'] = res_product.categ_id.property_account_expense_categ_id.id
                                                _logger.info("Creation for invoice lines ---------------> {}".format(dict_ol))
                                                create_p = self.env['account.move.line'].create(dict_ol)
                                                _logger.info("After creation ---------->{}".format(create_p))
                                                if create_p:
                                                    self.quickbooks_last_vendor_bill_imported_id = cust.get('Id')

                                        if i.get('AccountBasedExpenseLineDetail'):
                                            dict_al = {}
                                            dict_al['move_id'] = invoice_obj.id
                                            if i.get('Id'):
                                                dict_al['qb_id'] = int(i.get('Id'))
                                                dict_al['tax_ids'] = None
                                                dict_al['quantity'] = 1

                                            if i.get('Amount'):
                                                dict_al['price_unit'] = float(i.get('Amount'))
                                            else:
                                                dict_al['price_unit'] = 0.0

                                            if i.get('Description'):
                                                dict_al['name'] = i.get('Description')
                                            else:
                                                dict_al['name'] = 'NA'

                                            if i.get('AccountBasedExpenseLineDetail').get('AccountRef'):
                                                account = self.env['account.account'].search([('qbo_id', '=', i.get(
                                                    'AccountBasedExpenseLineDetail').get('AccountRef').get('value'))])
                                                dict_al['account_id'] = account.id

                                            create_p = self.env['account.move.line'].create(dict_al)
                                            if create_p:
                                                company.quickbooks_last_vendor_bill_imported_id = cust.get('Id')
                                    if cust.get('Balance') == 0:
                                        if invoice_obj.state == 'draft':
                                            invoice_obj.action_invoice_open()
                                            invoice_obj.write({
                                                'amount_residual': cust.get('Balance'),
                                                'amount_residual_signed': cust.get('Balance')
                                            })
                            else:
                                _logger.info("Bill exists!!!")
                                res_partner = self.env['res.partner'].search(
                                    [('qbo_vendor_id', '=', cust.get('VendorRef').get('value'))])
                                _logger.info("Partner is -----------> {}".format(res_partner))
                                if res_partner:
                                    dict_i = {}

                                    if cust.get('Id'):
                                        dict_i['partner_id'] = res_partner.id
                                        dict_i['qbo_invoice_id'] = cust.get('Id')
                                        dict_i['company_id'] = self.id

                                        dict_i['type'] = 'in_invoice'
                                    if cust.get('CurrencyRef'):
                                        if cust.get('CurrencyRef').get('value'):
                                            currency = self.env['res.currency'].search(
                                                [('name', '=', cust.get('CurrencyRef').get('value'))], limit=1)
                                            dict_i['currency_id'] = currency.id

                                    if res_partner.customer:
                                        sale = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
                                        if sale:
                                            dict_i['journal_id'] = sale.id
                                    if res_partner.supplier:
                                        purchase = self.env['account.journal'].search([('type', '=', 'purchase')],
                                                                                      limit=1)
                                        if purchase:
                                            dict_i['journal_id'] = purchase.id

                                        dict_i['reference_type'] = ''
                                    if cust.get('TotalAmt'):
                                        dict_i['total'] = cust.get('TotalAmt')
                                    # if cust.get('DocNumber'):
                                    #     dict_i['number'] = cust.get('DocNumber')

                                    # if cust.get('Balance'):
                                    #     if cust.get('Balance') != 0.0:
                                            # if not bill.payments_widget:
                                            #     dict_i['state'] = 'draft'
                                            # else:
                                            #     print"\n\npayments_widget :------------------> ",bill,bill.payments_widget
                                    # else:
                                    if not cust.get('Balance'):
                                        if bill.state == 'draft':
                                            bill.action_invoice_open()
                                        # dict_i['state'] = 'paid'

                                    if cust.get('Balance'):
                                        dict_i['amount_residual'] = cust.get('Balance')
                                        dict_i['amount_residual_signed'] = cust.get('Balance')
                                    else:
                                        dict_i['amount_residual'] = 0.0
                                        dict_i['amount_residual_signed'] = 0.0

                                    if cust.get('DueDate'):
                                        dict_i['invoice_date_due'] = cust.get('DueDate')
                                    if cust.get('TxnDate'):
                                        dict_i['invoice_date'] = cust.get('TxnDate')

                                    ele_in_list = len(cust.get('Line'))
                                    dict_t = cust.get('Line')[ele_in_list - 1]
#                                     if dict_t.get('DiscountLineDetail'):
#                                         dict_i['check'] = True
#
#                                         if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                             dict_i['discount_type'] = 'percentage'
#                                             dict_i['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                             dict_i['percentage_amt'] = dict_t.get('Amount')
#                                         else:
#                                             dict_i['discount_type'] = 'value'
#                                             dict_i['amount'] = dict_t.get('Amount')

                                    if cust.get('Amount'):
                                        dict_i['amount_total'] = cust.get('Amount')
                                    write_inv = bill.write(dict_i)
                                    if write_inv:
                                        _logger.info('Vendor Bill Updated Successfully :: %s', cust.get('Id'))

                                    bill._compute_residual()
                                    for i in cust.get('Line'):

                                        if i.get('ItemBasedExpenseLineDetail'):
                                            res_product = self.env['product.product'].search([('qbo_product_id', '=',
                                                                                               i.get(
                                                                                                   'ItemBasedExpenseLineDetail').get(
                                                                                                   'ItemRef').get(
                                                                                                   'value'))])
                                            if res_product:
                                                p_order_line = self.env['account.move.line'].search(
                                                    ['&', ('product_id', '=', res_product.id),
                                                     (('move_id', '=', bill.id))])

                                                if p_order_line:

                                                    if i.get('Id'):
                                                        ol_qb_id = int(i.get('Id'))

                                                    if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                        qty = i.get('ItemBasedExpenseLineDetail').get('Qty')

                                                    if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                        sp = float(
                                                            i.get('ItemBasedExpenseLineDetail').get('UnitPrice'))
                                                    else:
                                                        if not i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                            qty = 1
                                                            sp = float(
                                                                i.get('Amount'))
                                                        else:
                                                            sp = 0.0

                                                    if i.get('Description'):
                                                        description = i.get('Description')
                                                    else:
                                                        description = 'NA'

                                                    # create_p = self.env['account.move.line'].write(dict_ol)

                                                    create_iv = self.env['account.move.line'].search(
                                                        ['&', ('qb_id', '=', int(i.get('Id'))),
                                                         (('move_id', '=', bill.id))])
                                                    if create_iv:
                                                        data_dict = {

                                                            'product_id': res_product.id,
                                                            'name': description,
                                                            'quantity': qty,
                                                            'qb_id': ol_qb_id,
                                                            'price_unit': sp,
                                                            'tax_ids': None,
                                                        }
                                                        if res_product.property_account_expense_id:
                                                            _logger.info("ATTACHING product expense account")
                                                            data_dict.update({'account_id' : res_product.property_account_expense_id.id})
                                                        else:
                                                            _logger.info("ATTACHING category expense account")
                                                            data_dict.update({'account_id' : res_product.categ_id.property_account_expense_categ_id.id})
                                                        res = create_iv.write(data_dict)

                                                    # if discount_amt > 0:
                                                    #     create_iv.write({
                                                    #         'discount': discount_amt
                                                    #     })

                                                    if create_iv:
                                                        _logger.info("Invoice created...")
                                                        company.quickbooks_last_vendor_bill_imported_id = cust.get('Id')

                                                else:
                                                    dict_ol = {}

                                                    dict_ol.clear()
                                                    dict_ol['move_id'] = bill.id
                                                    dict_ol['product_id'] = res_product.id

                                                    if i.get('Id'):
                                                        dict_ol['qb_id'] = int(i.get('Id'))
                                                        dict_ol['tax_ids'] = None

                                                    if i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                        dict_ol['quantity'] = i.get('ItemBasedExpenseLineDetail').get(
                                                            'Qty')

                                                    if i.get('ItemBasedExpenseLineDetail').get('UnitPrice'):
                                                        dict_ol['price_unit'] = float(
                                                            i.get('ItemBasedExpenseLineDetail').get('UnitPrice'))
                                                    else:
                                                        if not i.get('ItemBasedExpenseLineDetail').get('Qty'):
                                                            dict_ol['quantity'] = 1
                                                            dict_ol['price_unit'] = float(
                                                                i.get('Amount'))
                                                        else:
                                                            dict_ol['price_unit'] = 0.0

                                                    # dict_ol['date_due'] = cust.get('TxnDate')

                                                    if i.get('Description'):
                                                        dict_ol['name'] = i.get('Description')
                                                    else:
                                                        dict_ol['name'] = 'NA'
                                                    
                                                    if res_product.property_account_expense_id:
                                                        dict_ol['account_id'] = res_product.property_account_expense_id.id
                                                        _logger.info("Attached from product ")
                                                    else:
                                                        dict_ol['account_id'] = res_product.categ_id.property_account_expense_categ_id.id

                                                    create_p = self.env['account.move.line'].create(dict_ol)
                                                    if create_p:
                                                        company.quickbooks_last_vendor_bill_imported_id = cust.get('Id')
                                        if i.get('AccountBasedExpenseLineDetail'):
                                            account_account = self.env['account.account'].search([('qbo_id', '=',
                                                                                                   i.get(
                                                                                                       'AccountBasedExpenseLineDetail').get(
                                                                                                       'AccountRef').get(
                                                                                                       'value'))])
                                            if account_account:
                                                a_order_line = self.env['account.move.line'].search(
                                                    ['&', ('account_id', '=', account_account.id),
                                                     (('move_id', '=', bill.id))])
                                                dict_al = {}
                                                if i.get('Id'):
                                                    dict_al['qb_id'] = int(i.get('Id'))
                                                    dict_al['tax_ids'] = None
                                                    dict_al['quantity'] = 1

                                                if i.get('Amount'):
                                                    dict_al['price_unit'] = float(i.get('Amount'))
                                                else:
                                                    dict_al['price_unit'] = 0.0

                                                if i.get('Description'):
                                                    dict_al['name'] = i.get('Description')
                                                else:
                                                    dict_al['name'] = 'NA'

                                                if i.get('AccountBasedExpenseLineDetail').get('AccountRef'):
                                                    account = self.env['account.account'].search([('qbo_id', '=', i.get(
                                                        'AccountBasedExpenseLineDetail').get('AccountRef').get(
                                                        'value'))])
                                                    if account:
                                                        dict_al['account_id'] = account.id
                                                        _logger.info("Attaching account id from AccountBasedExpenseLineDetail")
                                                    else:
                                                        _logger.error("Unable to fetch Account Based Expense Line Detail")

                                                if not a_order_line:
                                                    dict_al['move_id'] = bill.id
                                                    _logger.info("Account invoice line dict is ---------> {}".format(dict_al))
                                                    create_p = self.env['account.move.line'].create(dict_al)
                                                    if create_p:
                                                        _logger.info("Creation of invoice lines of vendor bills --------------- {}".format(create_p))
                                                        company.quickbooks_last_vendor_bill_imported_id = cust.get('Id')
                                                else:
                                                    _logger.info("Redirecting else part account.move.line")
                                                    create_p = self.env['account.move.line'].write(dict_al)
                                                    if create_p:
                                                        _logger.info("Updation  of invoice lines of vendor bills --------------- {}".format(create_p))

                                                        company.quickbooks_last_vendor_bill_imported_id = cust.get('Id')
            else:
                _logger.warning(_('Empty data'))
                
                
                
                
    ###################IMPORT CREDIT MEMO###########################################
    # @api.multi
    def import_credit_memo_1(self):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company.access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + company.access_token
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'

            query = "select * from CreditMemo WHERE Id > '%s' order by Id" % (company.quickbooks_last_credit_note_imported_id)

            data = requests.request('GET', self.url + str(self.realm_id) + "/query?query=" + query,
                                    headers=headers)
            if data:
                recs = []
                parsed_data = json.loads(str(data.text))
                count = 0

                if parsed_data:
                    if parsed_data.get('QueryResponse') and parsed_data.get('QueryResponse').get('CreditMemo'):
                        for cust in parsed_data.get('QueryResponse').get('CreditMemo'):
                            return_val = self.check_account_id(cust)
                            if return_val:
                                line_present = self.check_if_lines_present(cust)
                                _logger.info('ORDER LINES PRESENT IN INVOICE :: %s', line_present)
                                if not line_present:
                                    continue

                                count = count + 1
                                account_invoice = self.env['account.move'].search([('qbo_invoice_id', '=', cust.get('Id'))])
                                _logger.info("ACC invoice is -----> {}".format(account_invoice))
                                if not account_invoice:

                                    res_partner = self.env['res.partner'].search([('qbo_customer_id', '=', cust.get('CustomerRef').get('value'))])
                                    _logger.info("Partner is ---> {}".format(res_partner))
                                    if res_partner:
                                        dict_i = {}

                                        if cust.get('Id'):
                                            dict_i['partner_id'] = res_partner.id
                                            dict_i['qbo_invoice_id'] = cust.get('Id')
                                            dict_i['type'] = 'out_refund'

                                            # dict_i['name'] = "INVOICE"
                                            # dict_i['account_id'] = 0
                                            dict_i['company_id'] = self.id

                                        if cust.get('CurrencyRef'):
                                            if cust.get('CurrencyRef').get('value'):
                                                currency = self.env['res.currency'].search(
                                                    [('name', '=', cust.get('CurrencyRef').get('value'))], limit=1)
                                                dict_i['currency_id'] = currency.id

                                        if res_partner.customer_rank:
                                            sale = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
                                            if sale:
                                                dict_i['journal_id'] = sale.id
                                            else:
                                                sale = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
                                                if sale:
                                                    dict_i['journal_id'] = sale.id
                                        if res_partner.supplier_rank:
                                            purchase = self.env['account.journal'].search([('type', '=', 'purchase')],
                                                                                          limit=1)
                                            if purchase:
                                                dict_i['journal_id'] = purchase.id
                                            else:
                                                purchase = self.env['account.journal'].search([('type', '=', 'bank')],
                                                                                          limit=1)
                                                if purchase:
                                                    dict_i['journal_id'] = purchase.id

                                            # dict_i['journal_id'] = 1
                                            dict_i['reference_type'] = ''

                                        if cust.get('DocNumber'):
                                            dict_i['name'] = cust.get('DocNumber')
                                            # dict_i['number'] = cust.get('DocNumber')

                                        if cust.get('Balance'):
                                            dict_i['state'] = 'draft'
                                            dict_i['amount_residual'] = cust.get('Balance')
                                            dict_i['amount_residual_signed'] = cust.get('Balance')
                                            # dict_i['residual'] = cust.get('Balance')
                                            # dict_i['residual_signed'] = cust.get('Balance')
                                        else:
                                            dict_i['amount_residual'] = 0.0
                                            dict_i['amount_residual_signed'] = 0.0

                                        if cust.get('DueDate'):
                                            dict_i['invoice_date_due'] = cust.get('DueDate')
                                        if cust.get('TxnDate'):
                                            dict_i['invoice_date'] = cust.get('TxnDate')

                                        ele_in_list = len(cust.get('Line'))
                                        #       ele_in_list)
                                        dict_t = cust.get('Line')[ele_in_list - 1]
#                                         if dict_t.get('DiscountLineDetail'):
#                                             dict_i['check'] = True
#
#                                             if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                                 dict_i['discount_type'] = 'percentage'
#                                                 dict_i['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                                 dict_i['percentage_amt'] = dict_t.get('Amount')
#                                             else:
#                                                 dict_i['discount_type'] = 'value'
#                                                 dict_i['amount'] = dict_t.get('Amount')

                                        # if cust.get('TotalTax'):
                                        #     dict_i['amount_tax'] = cust.get('TotalTax')
                                        #
                                        if cust.get('TotalAmt'):
                                            dict_i['total'] = cust.get('TotalAmt')

                                        _logger.info("Dictionary for creation is ---> {}".format(dict_i))
                                        invoice_obj = self.env['account.move'].create(dict_i)
                                        _logger.info("Invoice obj is -----> {}".format(invoice_obj))
                                        if invoice_obj:
#                                             self._cr.commit()
                                            _logger.info('Credit Memo  Created Successfully..!! :: %s', invoice_obj)

                                        # if invoice_obj:
                                        #     tax_call = invoice_obj._onchange_invoice_line_ids()
                                        #     print("TAX CALL----------->",tax_call)
                                        custom_tax_id = None
                                        # print"\n\n\n\nLINE : -----------------> ", cust.get('Line')

                                        for i in cust.get('Line'):
                                            dict_ol = {}
                                            if cust.get('TxnTaxDetail').get('TxnTaxCodeRef'):
                                                if cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value'):

                                                    qb_tax_id = cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value')
                                                    record = self.env['account.tax']
                                                    tax = record.search([('qbo_tax_id', '=', qb_tax_id)])
                                                    if tax:
                                                        custom_tax_id = [(6, 0, [tax.id])]
                                                        _logger.info("TAX ATTACHED {}".format(tax.id))
                                                    else:
                                                        custom_tax_id = None

                                            if i.get('SalesItemLineDetail'):
                                                res_product = self.env['product.product'].search(
                                                    [('qbo_product_id', '=', i.get('SalesItemLineDetail').get('ItemRef').get('value'))])
                                                if res_product:

                                                    dict_ol.clear()
                                                    dict_ol['move_id'] = invoice_obj.id

                                                    dict_ol['product_id'] = res_product.id

                                                    if i.get('Id'):
                                                        dict_ol['qb_id'] = int(i.get('Id'))

                                                    # ---------------------------TAX--------------------------------------
                                                    if i.get('SalesItemLineDetail').get('TaxCodeRef'):

                                                        tax_val = i.get('SalesItemLineDetail').get(
                                                            'TaxCodeRef').get(
                                                            'value')
                                                        if tax_val == 'TAX':

                                                            dict_ol['tax_ids'] = custom_tax_id
                                                        else:
                                                            dict_ol['tax_ids'] = None

                                                    if i.get('SalesItemLineDetail').get('Qty'):
                                                        dict_ol['quantity'] = i.get('SalesItemLineDetail').get('Qty')

                                                    if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                        dict_ol['price_unit'] = float(i.get('SalesItemLineDetail').get('UnitPrice'))
                                                    else:
                                                        if not i.get('SalesItemLineDetail').get('Qty'):
                                                            dict_ol['quantity'] = 1
                                                            dict_ol['price_unit'] = float(
                                                                i.get('Amount'))
                                                        else:
                                                            dict_ol['price_unit'] = 0

                                                    if i.get('Description'):
                                                        dict_ol['name'] = i.get('Description')
                                                    else:
                                                        dict_ol['name'] = 'NA'

                                                    if res_product.property_account_income_id:
                                                        dict_ol['account_id'] = res_product.property_account_income_id.id
                                                        _logger.info("PRODUCT has income account set")
                                                    else:
                                                        dict_ol['account_id'] = res_product.categ_id.property_account_income_categ_id.id
                                                        _logger.info("No Income account was set, taking from product category..")
                                                    if 'account_id' in dict_ol:    
                                                        _logger.info("\n\n Invoice Line is  ---> {}".format(dict_ol))
                                                        create_p = self.env['account.move.line'].create(dict_ol)
                                                        if create_p:
                                                            self._cr.commit()
                                                            _logger.info("Invoice Line Committed!!!")
                                                            create_p.move_id._onchange_invoice_line_ids()
                                                            company.quickbooks_last_invoice_imported_id = cust.get('Id')
                                                        else:
                                                            _logger.error("Invoice line was not created.")
                                                    else:
                                                        _logger.error("NO ACCOUNT ID WAS ATTACHED !")
                                        if cust.get('Balance') == 0:
                                            if invoice_obj.state == 'draft':
                                                invoice_obj.action_invoice_open()
                                                if cust.get('DocNumber'):
                                                    invoice_obj.write({'name': cust.get('DocNumber'),
                                                                       'amount_residual': cust.get('Balance'),
                                                                       'amount_residual_signed': cust.get('Balance')})

                                else:
                                    res_partner = self.env['res.partner'].search([('qbo_customer_id', '=', cust.get('CustomerRef').get('value'))])

                                    if res_partner:
                                        dict_i = {}

                                        if cust.get('Id'):
                                            dict_i['partner_id'] = res_partner.id
                                            dict_i['qbo_invoice_id'] = cust.get('Id')
                                            # dict_i['name'] = "INVOICE"
                                            # dict_i['account_id'] = 0
                                            dict_i['company_id'] = self.id
                                            # dict_i['type'] = 'out_refund'

                                        if cust.get('CurrencyRef'):
                                            if cust.get('CurrencyRef').get('value'):
                                                currency = self.env['res.currency'].search(
                                                    [('name', '=', cust.get('CurrencyRef').get('value'))], limit=1)
                                                dict_i['currency_id'] = currency.id

                                        if res_partner.customer:
                                            sale = self.env['account.journal'].search([('type', '=', 'sale')],
                                                                                      limit=1)
                                            if sale:
                                                dict_i['journal_id'] = sale.id
                                        if res_partner.supplier:
                                            purchase = self.env['account.journal'].search(
                                                [('type', '=', 'purchase')],
                                                limit=1)
                                            if purchase:
                                                dict_i['journal_id'] = purchase.id

                                            # dict_i['journal_id'] = 1
                                            dict_i['reference_type'] = ''

                                        if cust.get('TotalAmt'):
                                            dict_i['total'] = cust.get('TotalAmt')
                                        if cust.get('DocNumber'):
                                            dict_i['name'] = cust.get('DocNumber')
                                            # dict_i['number'] = cust.get('DocNumber')

                                        if cust.get('Balance'):
                                            # if not account_invoice.payments_widget:
                                            #     dict_i['state'] = 'draft'
                                            # else:
                                            #     print"payments_widget :------------------> ",account_invoice,account_invoice.payments_widget
                                            dict_i['amount_residual'] = cust.get('Balance')
                                            dict_i['amount_residual_signed'] = cust.get('Balance')
                                            # dict_i['residual'] = cust.get('Balance')
                                            # dict_i['residual_signed'] = cust.get('Balance')
                                        else:
                                            # dict_i['state'] = 'paid'
                                            dict_i['amount_residual'] = 0.0
                                            dict_i['amount_residual_signed'] = 0.0
                                            # dict_i['residual'] = 0.0
                                            # dict_i['residual_signed'] = 0.0
                                            if account_invoice.state == 'draft':
                                                account_invoice.action_invoice_open()

                                        if cust.get('DueDate'):
                                            dict_i['invoice_date_due'] = cust.get('DueDate')
                                        if cust.get('TxnDate'):
                                            dict_i['invoice_date'] = cust.get('TxnDate')

                                        ele_in_list = len(cust.get('Line'))
                                        dict_t = cust.get('Line')[ele_in_list - 1]
#                                         if dict_t.get('DiscountLineDetail'):
#                                             dict_i['check'] = True
#
#                                             if dict_t.get('DiscountLineDetail').get('DiscountPercent'):
#                                                 dict_i['discount_type'] = 'percentage'
#                                                 dict_i['amount'] = dict_t.get('DiscountLineDetail').get('DiscountPercent')
#                                                 dict_i['percentage_amt'] = dict_t.get('Amount')
#                                             else:
#                                                 dict_i['discount_type'] = 'value'
#                                                 dict_i['amount'] = dict_t.get('Amount')

                                        write_inv = account_invoice.write(dict_i)
                                        if write_inv:
                                            _logger.info('Credit Memo Updated Successfully..!! :: %s', cust.get('Id'))

                                        account_invoice._onchange_invoice_line_ids()

                                        custom_tax_id_id = None
                                        custom_tax_id = None
                                        # print"\n\n\n\nLINE : -----------------> ", cust.get('Line')

                                        for i in cust.get('Line'):
                                            if cust.get('TxnTaxDetail'):
                                                if cust.get('TxnTaxDetail').get('TxnTaxCodeRef'):
                                                    if cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value'):

                                                        qb_tax_id = cust.get('TxnTaxDetail').get('TxnTaxCodeRef').get('value')
                                                        record = self.env['account.tax']
                                                        tax = record.search([('qbo_tax_id', '=', qb_tax_id)])
                                                        if tax:
                                                            custom_tax_id = [(6, 0, [tax.id])]
                                                        else:
                                                            custom_tax_id = None

                                            if i.get('SalesItemLineDetail'):
                                                res_product = self.env['product.product'].search(
                                                    [('qbo_product_id', '=', i.get('SalesItemLineDetail').get('ItemRef').get('value'))])
                                                
                                                if res_product:
                                                    p_order_line = self.env['account.move.line'].search(
                                                        ['&', ('product_id', '=', res_product.id),
                                                         (('move_id', '=', account_invoice.id))])

                                                    if p_order_line:

                                                        if i.get('Id'):
                                                            ol_qb_id = int(i.get('Id'))

                                                        if i.get('SalesItemLineDetail').get('Qty'):
                                                            qty = i.get('SalesItemLineDetail').get('Qty')
                                                        else:
                                                            qty = 0

                                                        if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                            sp = float(
                                                                i.get('SalesItemLineDetail').get('UnitPrice'))
                                                        else:
                                                            if not i.get('SalesItemLineDetail').get('Qty'):
                                                                qty = 1
                                                                sp = float(
                                                                    i.get('Amount'))
                                                            else:
                                                                sp = 0.0

                                                        if i.get('SalesItemLineDetail').get('TaxCodeRef'):

                                                            # print("TAX AVAILABLE : ",
                                                            #       i.get('SalesItemLineDetail').get('TaxCodeRef').get(
                                                            #           'value'))
                                                            tax_val = i.get('SalesItemLineDetail').get(
                                                                'TaxCodeRef').get(
                                                                'value')
                                                            if tax_val == 'TAX':

                                                                custom_tax_id_id = custom_tax_id
                                                            else:
                                                                custom_tax_id_id = None

                                                        if i.get('Description'):
                                                            description = i.get('Description')
                                                        else:
                                                            description = 'NA'
                                                        
                                                        income_id = None
                                                        
                                                        if res_product.property_account_income_id.id:
                                                            income_id = res_product.property_account_income_id.id
                                                        else:
                                                            income_id = res_product.categ_id.property_account_income_categ_id.id

                                                        # create_p = self.env['account.move.line'].write(dict_ol)

                                                        create_iv = self.env['account.move.line'].search(
                                                            ['&', ('qb_id', '=', int(i.get('Id'))),
                                                             (('move_id', '=', account_invoice.id))])
                                                        # search([['qb_id', '=', i.get('Id')]])
                                                        if create_iv:
                                                            res = create_iv.write({

                                                                'product_id': res_product.id,
                                                                'name': description,
                                                                'quantity': qty,
                                                                'account_id': income_id ,
                                                                'qb_id': ol_qb_id,
                                                                'price_unit': sp,
                                                                'tax_ids': custom_tax_id_id,
                                                            })
                                                        
                                                        if create_iv:
                                                            company.quickbooks_last_credit_note_imported_id = cust.get('Id')

                                                    else:

                                                        dict_ol = {}
                                                        res_product_acc = self.env['product.product'].search([])

    #                                                     print("**********PRODUCT ACCOUNT CHECK************",res_product_acc.property_account_income_id)
                                                        dict_ol.clear()
                                                        dict_ol['move_id'] = account_invoice.id
                                                        dict_ol['product_id'] = res_product.id

                                                        if i.get('Id'):
                                                            dict_ol['qb_id'] = int(i.get('Id'))

                                                        if i.get('SalesItemLineDetail').get('TaxCodeRef'):

                                                            tax_val = i.get('SalesItemLineDetail').get(
                                                                'TaxCodeRef').get(
                                                                'value')
                                                            if tax_val == 'TAX':
                                                                dict_ol['tax_ids'] = custom_tax_id
                                                            else:
                                                                dict_ol['tax_ids'] = None

                                                        if i.get('SalesItemLineDetail').get('Qty'):
                                                            dict_ol['quantity'] = i.get('SalesItemLineDetail').get(
                                                                'Qty')

                                                        if i.get('SalesItemLineDetail').get('UnitPrice'):
                                                            dict_ol['price_unit'] = float(
                                                                i.get('SalesItemLineDetail').get('UnitPrice'))
                                                        else:
                                                            if not i.get('SalesItemLineDetail').get('Qty'):
                                                                dict_ol['quantity'] = 1
                                                                dict_ol['price_unit'] = float(
                                                                    i.get('Amount'))
                                                            else:
                                                                dict_ol['price_unit'] = 0.0

                                                        if i.get('Description'):
                                                            dict_ol['name'] = i.get('Description')
                                                        else:
                                                            dict_ol['name'] = 'NA'
                                                        if res_product.property_account_income_id:
                                                            dict_ol['account_id'] = res_product.property_account_income_id.id
                                                        else:
                                                            dict_ol['account_id'] = res_product.categ_id.property_account_income_categ_id.id

                                                            create_p = self.env['account.move.line'].create(dict_ol)
                                                            if create_p:
                                                                company.quickbooks_last_credit_note_imported_id = cust.get('Id')
            else:
                _logger.warning(_('Empty data'))
              

    # @api.multi
    def export_customers(self):
        res_partner = self.env['res.partner'].search([])

        for contact in res_partner:
            if contact.id == 1 or contact.id == 3:
                _logger.info(_("There is no any record to be exported."))
            else:
                if contact.customer_rank and contact.type == 'contact':
                    contact.exportCustomer()

    # @api.multi
    def export_vendors(self):
        res_partner = self.env['res.partner'].search([])
        for contact in res_partner:
            if contact.id == 1 or contact.id == 3:
                _logger.info(_("There is no any record to be exported."))
            else:
                if contact.supplier_rank:
                    contact.exportVendor()

    # @api.multi
    def export_accounts(self):
        accounts = self.env['account.account'].search([])

        for account in accounts:
            if not account.qbo_id:
                account.export_to_qbo()

    # @api.multi
    def export_tax(self):
        taxes = self.env['account.tax'].search([])
        for tax in taxes:
            tax.export_to_qbo()

    # @api.multi
    # def export_tax_agency(self):
    #     taxes = self.env['account.tax.agency'].search([])
    #     print("TAX AGENCY : ----------------------> ", taxes)
    #     for tax in taxes:
    #         print("AGENCY : ----------------------> ", tax)
    #         tax.export_to_qbo()

    # @api.multi
    def export_products(self):
        products = self.env['product.product'].search([])
        if not products:
            raise Warning('There is no any record to be exported.')
        for product in products:
            product.export_product_to_qbo()

    # @api.multi
    def export_payment_method(self):
        payment_method = self.env['account.journal'].search([('type','in',['cash','bank'])])
        if not payment_method:
            raise Warning('There is no any record to be exported.')
        for method in payment_method:
            if not method.qbo_method_id:
                # print("\n\n--- method ---",method)
                method.export_to_qbo()
            else:
                _logger.info(_("There is no any record to be exported."))

    # @api.multi
    def export_payment_terms(self):
        payment_term = self.env['account.payment.term'].search([])
        if not payment_term:
            raise Warning('There is no any record to be exported.')
        for term in payment_term:
            term.export_payment_term_to_quickbooks()

    # @api.multi
    def export_sale_order(self):
        sales = self.env['sale.order'].search([])
        if not sales:
            raise Warning('There is no any record to be exported.')
        for sale in sales:
            if sale.quickbook_id and sale.state == 'sale':
                _logger.info(_("Sale Order is already exported to QBO. %s" % sale))
            else:
                sale.exportSaleOrder()

    # @api.multi
    def export_invoice(self):
        invoices = self.env['account.move'].search([])
        if not invoices:
            raise Warning('There is no any record to be exported.')
        for inv in invoices:
            if inv.partner_id.customer_rank:
                if inv.state == 'open' and inv.qbo_invoice_id:
                    _logger.info(_("Invoice is already exported to QBO. %s" % inv))
                else:
                    inv.export_to_qbo()

    # @api.multi
    def export_purchase_order(self):
        purchase = self.env['purchase.order'].search([])
        if not purchase:
            raise Warning('There is no any record to be exported.')
        for order in purchase:
            if order.state == 'purchase' and order.quickbook_id:
                _logger.info(_("Purchase Order is already exported to QBO. %s" % order))
            else:
                order.exportPurchaseOrder()

    # @api.multi
    def export_vendor_bill(self):
        invoices = self.env['account.move'].search([])
        if not invoices:
            raise Warning('There is no any record to be exported.')
        for inv in invoices:
            if inv.partner_id.supplier_rank:
                if inv.state == 'open' and inv.qbo_invoice_id:
                    _logger.info(_("Invoice is already exported to QBO. %s" % inv))
                else:
                    inv.export_to_qbo()

    # @api.multi
    def export_department(self):
        department = self.env['hr.department'].search([])
        if not department:
            raise Warning('There is no any record to be exported.')
        for dept in department:
            dept.exportDepartment()

    # @api.multi
    def export_employee(self):
        employee = self.env['hr.employee'].search([])
        if not employee:
            raise Warning('There is no any record to be exported.')
        for emp in employee:
            emp.export_Employees_to_qbo()
