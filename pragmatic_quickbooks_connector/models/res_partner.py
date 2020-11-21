from odoo import api, fields, models, _
import requests
import json
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class ResCountry(models.Model):
    _inherit = "res.country"

    @api.model
    def get_country_ref(self, country_name):
        """
        This method take country name as an argument and return county id
        :param country_name: name of the country
        :rtype int: return a recordset id
        """
        try:
            country = self.search([('name', '=', country_name)], limit=1)
            if not country:
                _logger.info("Country not found in Odoo")
                # country = self.create({'name': country_name})
            else:
                return country.id
        except Exception:
            return False

class ResCountryState(models.Model):
    _inherit = "res.country.state"

    @api.model
    def get_state_ref(self, state_name, country_name):
        """
        This method take state name as an argument and return state id
        :param state_name: name of state
        :param country_name: name of country
        :rtype int: return a recordset id
        """
        try:
            if country_name:
                _logger.info(_("QBO State : %s" % (state_name)))
                _logger.info(_("QBO Country : %s" % (country_name)))

                country_id = self.env['res.country'].get_country_ref(country_name)
                if not country_id:
                    return False
                state = self.search([('name', '=', state_name),('country_id', '=', country_id)], limit=1)
                if not state:
                    _logger.info("State not found in Odoo")
                    # state = self.create({'name': state_name, 'country_id': country_id, 'code': state_name})
                else:
                    return state.id
            else:
                return False
        except Exception:
            return False

class ResPartner(models.Model):
    _inherit = "res.partner"

    qbo_vendor_id = fields.Char("QBO Vendor Id", copy=False, help="QuickBooks database recordset id")
    qbo_customer_id = fields.Char("QBO Customer Id", copy=False, help="QuickBooks database recordset id")
    x_quickbooks_exported = fields.Boolean("Exported to Quickbooks ? ", default=False)
    x_quickbooks_updated = fields.Boolean("Updated in Quickbook ?", default=False)

    ''' For Import Partner'''
    
    @api.model
    def create(self, vals):
        if 'res_partner_search_mode' in self._context and self._context.get('res_partner_search_mode') == 'customer':
            vals['customer_rank'] = 1
        if 'res_partner_search_mode' in self._context and self._context.get('res_partner_search_mode') == 'supplier':
            vals['supplier_rank'] = 1
        res = super(ResPartner, self).create(vals)
        return res

    @api.model
    def attachCustomerTitle(self, title):
        res_partner_tile = self.env['res.partner.title']
        title_id = False
        if title:
            title_id = res_partner_tile.search([('name', '=', title)], limit=1)
            if not title_id:
                ''' Create New Title in Odoo '''
                create_id = res_partner_tile.create({'name': title})
                # create_id = title_id.id
                if create_id:
                    return create_id.id
            return title_id.id

    @api.model
    def get_parent_customer_ref(self, qbo_parent_id):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        partner = self.search([('qbo_customer_id', '=', qbo_parent_id)], limit=1)
        if not partner:
            url_str = company.get_import_query_url()
            url = url_str.get('url') + '/customer/' + qbo_parent_id
            data = requests.request('GET', url, headers=url_str.get('headers'))
            if data:
                partner = self.create_partner(data, is_customer=True)
        return partner.id

    @api.model
    def get_parent_vendor_ref(self, qbo_parent_id):
        company = self.env['res.users'].search([('id', '=', 2)]).company_id
        partner = self.search([('qbo_vendor_id', '=', qbo_parent_id)], limit=1)
        if not partner:
            url_str = company.get_import_query_url()
            url = url_str.get('url') + '/vendor/' + qbo_parent_id
            data = requests.request('GET', url, headers=url_str.get('headers'))
            if data:
                partner = self.create_partner(data, is_vendor=True)
        return partner.id

    @api.model
    def _prepare_partner_dict(self, partner, is_customer=False, is_vendor=False):

        vals = {
            'company_type': 'person' if partner.get('Job') else 'company',
            # 'name': partner.get('DisplayName'),
            'qbo_customer_id': partner.get('Id') if is_customer else '',
            'qbo_vendor_id': partner.get('Id') if is_vendor else '',
            # 'customer': is_customer,
            # 'supplier': is_vendor,
            'email': partner.get('PrimaryEmailAddr').get('Address') if partner.get('PrimaryEmailAddr') else '',
            'phone': partner.get('PrimaryPhone').get('FreeFormNumber') if partner.get('PrimaryPhone') else '',
            'mobile': partner.get('Mobile').get('FreeFormNumber') if partner.get('Mobile') else '',
            'website': partner.get('WebAddr').get('URI') if partner.get('WebAddr') else '',
            'active': partner.get('Active'),
            'comment': partner.get('Notes'),
        }

        # print ("is_customer -------------------------------------", is_customer)
        # print ("is_vendor ---------------------------------------", is_vendor)

        if is_customer:
            vals.update({'customer_rank': 1})
        if is_vendor:
            vals.update({'supplier_rank': 1})
        if partner.get('GivenName'):
            vals.update({'name': partner.get('GivenName')})
        if partner.get('MiddleName'):
            vals.update({'name': partner.get('MiddleName')})
        if partner.get('FamilyName'):
            vals.update({'name': partner.get('FamilyName')})
        if partner.get('GivenName') and partner.get('MiddleName'):
            vals.update({'name': partner.get('GivenName') + ' ' + partner.get('MiddleName')})
        if partner.get('MiddleName') and partner.get('FamilyName'):
            vals.update({'name': partner.get('MiddleName') + ' ' + partner.get('FamilyName')})
        if partner.get('GivenName') and partner.get('FamilyName'):
            vals.update({'name': partner.get('GivenName') + ' ' + partner.get('FamilyName')})
        if partner.get('GivenName') and partner.get('MiddleName') and partner.get('FamilyName'):
            vals.update(
                {'name': partner.get('GivenName') + ' ' + partner.get('MiddleName') + ' ' + partner.get('FamilyName')})

        if not partner.get('GivenName'):
            vals.update({'name': partner.get('DisplayName')})

        if partner.get('Title'):
            ''' If Title is present then first check in odoo if title exists or not
            if exists attach Id of tile else create new and attach its ID'''

            title = self.attachCustomerTitle(partner.get('Title'))
            vals.update({'title': title})

        #         child_ids = []
        if 'BillAddr' in partner and partner.get('BillAddr'):
            address_vals = {
                'street': partner.get('BillAddr').get('Line1') or '',
                'street2': partner.get('BillAddr').get('Line2') or '',
                'city': partner.get('BillAddr').get('City') or '',
                'zip': partner.get('BillAddr').get('PostalCode') or '',
                'state_id': self.env['res.country.state'].get_state_ref(
                    partner.get('BillAddr').get('CountrySubDivisionCode'),
                    partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get(
                    'CountrySubDivisionCode') and partner.get('BillAddr').get('Country') else False,
                'country_id': self.env['res.country'].get_country_ref(
                    partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get('Country') else False,
            }
            vals.update(address_vals)

        if 'ParentRef' in partner:
            if is_customer:
                vals.update({'parent_id': self.get_parent_customer_ref(partner.get('ParentRef').get('value'))})
            if is_vendor:
                vals.update({'parent_id': self.get_parent_vendor_ref(partner.get('ParentRef').get('value'))})

        return vals

    @api.model
    def create_partner(self, data, is_customer=False, is_vendor=False):
        """Create partner object in odoo
        :param data: partner object response return by QBO
        :param is_customer: True if partner is a customer
        :param is_vendor: True if partener is a supplier/vendor
        :return int: last import QBO customer or vendor Id
        """
        res = json.loads(str(data.text))
        brw_partner = False
        if is_customer:
            if 'QueryResponse' in res:
                partners = res.get('QueryResponse').get('Customer', [])
            else:
                partners = [res.get('Customer')] or []
        elif is_vendor:
            if 'QueryResponse' in res:
                partners = res.get('QueryResponse').get('Vendor', [])
            else:
                partners = [res.get('Vendor')] or []
        else:
            partners = []

        for partner in partners:
            vals = self._prepare_partner_dict(partner, is_customer=is_customer, is_vendor=is_vendor)
            brw_partner = self.search([('qbo_customer_id', '=', partner.get('Id'))], limit=1)
            _logger.info("Browsing partner************ {}".format(brw_partner))
            if not brw_partner:
                _logger.info("Customer needs to be created")
                brw_partner = self.create(vals)

                if 'BillAddr' in partner and partner.get('BillAddr'):
                    address_vals = {
                        'street': partner.get('BillAddr').get('Line1') or '',
                        'street2': partner.get('BillAddr').get('Line2') or '',
                        'city': partner.get('BillAddr').get('City') or '',
                        'zip': partner.get('BillAddr').get('PostalCode') or '',
                        'state_id': self.env['res.country.state'].get_state_ref(
                            partner.get('BillAddr').get('CountrySubDivisionCode'),
                            partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get(
                            'CountrySubDivisionCode') and partner.get('BillAddr').get('Country') else False,
                        'country_id': self.env['res.country'].get_country_ref(
                            partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get(
                            'Country') else False,
                        'type': 'invoice',
                        'parent_id': brw_partner.id
                    }
                    # Create partner billing address
                    bill_addr = self.create(address_vals)

                if 'ShipAddr' in partner and partner.get('ShipAddr'):
                    address_vals = {
                        'street': partner.get('ShipAddr').get('Line1') or '',
                        'street2': partner.get('ShipAddr').get('Line2') or '',
                        'city': partner.get('ShipAddr').get('City') or '',
                        'zip': partner.get('ShipAddr').get('PostalCode') or '',
                        'state_id': self.env['res.country.state'].get_state_ref(
                            partner.get('ShipAddr').get('CountrySubDivisionCode'),
                            partner.get('ShipAddr').get('Country')) if partner.get('ShipAddr').get(
                            'CountrySubDivisionCode') and partner.get('ShipAddr').get('Country') else False,
                        'country_id': self.env['res.country'].get_country_ref(
                            partner.get('ShipAddr').get('Country')) if partner.get('ShipAddr').get(
                            'Country') else False,
                        'type': 'delivery',
                        'parent_id': brw_partner.id
                    }
                    # Create partner shipping address
                    ship_addr = self.create(address_vals)
                _logger.info(_("Partner created sucessfully! Partner Id: %s" % (brw_partner.id)))

            else:
                _logger.info("Customer needs to be updated")
                update_customer = self.env['ir.config_parameter'].sudo().get_param(
                    'pragmatic_quickbooks_connector.update_customer_import')
                if update_customer:
                    brw_partner.write(vals)
                    if 'BillAddr' in partner and partner.get('BillAddr'):
                        address_vals = {
                            'street': partner.get('BillAddr').get('Line1') or '',
                            'street2': partner.get('BillAddr').get('Line2') or '',
                            'city': partner.get('BillAddr').get('City') or '',
                            'zip': partner.get('BillAddr').get('PostalCode') or '',
                            'state_id': self.env['res.country.state'].get_state_ref(
                                partner.get('BillAddr').get('CountrySubDivisionCode'),
                                partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get(
                                'CountrySubDivisionCode') and partner.get('BillAddr').get('Country') else False,
                            'country_id': self.env['res.country'].get_country_ref(
                                partner.get('BillAddr').get('Country')) if partner.get('BillAddr').get(
                                'Country') else False,
                            'type': 'invoice',
                            'parent_id': brw_partner.id
                        }
                        # Create partner billing address
                        bill_addr = self.write(address_vals)

                    if 'ShipAddr' in partner and partner.get('ShipAddr'):
                        address_vals = {
                            'street': partner.get('ShipAddr').get('Line1') or '',
                            'street2': partner.get('ShipAddr').get('Line2') or '',
                            'city': partner.get('ShipAddr').get('City') or '',
                            'zip': partner.get('ShipAddr').get('PostalCode') or '',
                            'state_id': self.env['res.country.state'].get_state_ref(
                                partner.get('ShipAddr').get('CountrySubDivisionCode'),
                                partner.get('ShipAddr').get('Country')) if partner.get('ShipAddr').get(
                                'CountrySubDivisionCode') and partner.get('ShipAddr').get('Country') else False,
                            'country_id': self.env['res.country'].get_country_ref(
                                partner.get('ShipAddr').get('Country')) if partner.get('ShipAddr').get(
                                'Country') else False,
                            'type': 'delivery',
                            'parent_id': brw_partner.id
                        }
                        # Create partner billing address
                        ship_addr = self.write(address_vals)

                #             child_ids = []

                    _logger.info(_("Partner updated sucessfully! Partner Id: %s" % (brw_partner.id)))
        return brw_partner

    ''' Uncategorized '''

    @api.model
    def get_qbo_partner_ref(self, partner):
        if partner.customer_rank:
            if partner.qbo_customer_id or (partner.parent_id and partner.parent_id.qbo_customer_id):
                return partner.qbo_customer_id or partner.parent_id.qbo_customer_id
            else:
                self.export_single_Partner(partner)
                if partner.qbo_customer_id or (partner.parent_id and partner.parent_id.qbo_customer_id):
                    return partner.qbo_customer_id or partner.parent_id.qbo_customer_id
                # raise ValidationError(_("Partner is not exported to QBO"))
        else:
            if partner.qbo_vendor_id or (partner.parent_id and partner.parent_id.qbo_vendor_id):
                return partner.qbo_vendor_id or partner.parent_id.qbo_vendor_id
            else:
                self.export_single_Partner(partner)
                if partner.qbo_vendor_id or (partner.parent_id and partner.parent_id.qbo_vendor_id):
                    return partner.qbo_vendor_id or partner.parent_id.qbo_vendor_id
                # raise ValidationError(_("Partner is not exported to QBO"))

    ''' For Export Partner'''

    def sendDataToQuickbooksForUpdate(self, dict):

        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        ''' GET ACCESS TOKEN '''

        access_token = None
        realmId = None
        parsed_dict = json.dumps(dict)
        if company.access_token:
            access_token = company.access_token
        if company.realm_id:
            realmId = company.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

            result = requests.request('POST', company.url + str(realmId) + "/customer?operation=update", headers=headers, data=parsed_dict)
            if result.status_code == 200:
                parsed_result = result.json()
                if parsed_result.get('Customer').get('Id'):
                    self.x_quickbooks_updated = True
                    return parsed_result.get('Customer').get('Id')
                else:
                    return False
            else:
                self.env['qbo.logger'].create({
                    'odoo_name':dict.get('DisplayName'),
                    'odoo_object':'Customer',
                    'message': result.text,
                    'created_date': datetime.now(),
                })
                return False

    def sendDataToQuickbook(self, dict):

        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        ''' GET ACCESS TOKEN '''

        access_token = None
        realmId = None
        parsed_dict = json.dumps(dict)
        if company.access_token:
            access_token = company.access_token
        if company.realm_id:
            realmId = company.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

            result = requests.request('POST', company.url + str(realmId) + "/customer", headers=headers, data=parsed_dict)
            if result.status_code == 200:
                parsed_result = result.json()
                if parsed_result.get('Customer').get('Id'):
                    if self.parent_id:
                        self.parent_id.x_quickbooks_exported = True
                    if not self.parent_id:
                        self.x_quickbooks_exported = True
                    return parsed_result.get('Customer').get('Id')
                else:
                    return False
            else:
                self.env['qbo.logger'].create({
                    'odoo_name':dict.get('DisplayName'),
                    'odoo_object':'Customer',
                    'message': result.text,
                    'created_date': datetime.now(),
                })
                return False

    def sendVendorDataToQuickbooksForUpdate(self, dict):

        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        ''' GET ACCESS TOKEN '''

        access_token = None
        realmId = None
        parsed_dict = json.dumps(dict)
        if company.access_token:
            access_token = company.access_token
        if company.realm_id:
            realmId = company.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

            result = requests.request('POST', company.url + str(realmId) + "/vendor?operation=update", headers=headers, data=parsed_dict)
            if result.status_code == 200:
                parsed_result = result.json()
                if parsed_result.get('Vendor').get('Id'):
                    self.x_quickbooks_updated = True
                    return parsed_result.get('Vendor').get('Id')
                else:
                    return False
            else:
                self.env['qbo.logger'].create({
                    'odoo_name':dict.get('DisplayName'),
                    'odoo_object':'Vendor',
                    'message': result.text,
                    'created_date': datetime.now(),
                })
                return False

    def sendVendorDataToQuickbook(self, dict):

        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        ''' GET ACCESS TOKEN '''

        access_token = None
        realmId = None
        parsed_dict = json.dumps(dict)
        if company.access_token:
            access_token = company.access_token
        if company.realm_id:
            realmId = company.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

            result = requests.request('POST', company.url + str(realmId) + "/vendor", headers=headers, data=parsed_dict)
            if result.status_code == 200:
                parsed_result = result.json()
                if parsed_result.get('Vendor').get('Id'):
                    if self.parent_id:
                        self.parent_id.x_quickbooks_exported = True
                    if not self.parent_id:
                        self.x_quickbooks_exported = True
                    return parsed_result.get('Vendor').get('Id')
                else:
                    return False
            else:
                self.env['qbo.logger'].create({
                    'odoo_name':dict.get('DisplayName'),
                    'odoo_object':'Vendor',
                    'message': result.text,
                    'created_date': datetime.now(),
                })
                return False

    def prepareDictStructure(self, obj=False, record_type=False, customer_id_retrieved=False, is_update=False,
                             sync_token=False):
        data_object = None

        if obj:
            data_object = obj
        else:
            data_object = self

        ''' This Function Exports Record to Quickbooks '''
        dict = {}
        dict_phone = {}
        dict_email = {}
        dict_mobile = {}
        dict_billAddr = {}
        dict_shipAddr = {}
        dict_parent_ref = {}
        dict_job = {}

        if data_object.mobile:
            dict['Mobile'] = {'FreeFormNumber': str(data_object.mobile)}

        if data_object.website:
            dict['WebAddr'] = {'URI': str(data_object.website)}

        if data_object.comment:
            dict["Notes"] = data_object.comment
        #
        # if data_object.name:
        #     dict["GivenName"] = str(data_object.name)
        #     dict['DisplayName'] = str(data_object.display_name)

        if data_object.name:
            full_name = str(data_object.name)
            if len(full_name.split()) == 1:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = " "
                dict["FamilyName"] = " "
            if len(full_name.split()) == 2:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = " "
                dict["FamilyName"] = full_name.split()[1]

            if len(full_name.split()) == 3:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = full_name.split()[1]
                dict["FamilyName"] = full_name.split()[2]

            dict['DisplayName'] = str(data_object.name)
            dict['PrintOnCheckName'] = str(data_object.name)

        if data_object.title:
            dict["Title"] = data_object.title.name

        if data_object.email:
            dict_email["PrimaryEmailAddr"] = {'Address': str(data_object.email)}

        if data_object.phone:
            dict_phone["PrimaryPhone"] = {'FreeFormNumber': str(data_object.phone)}

        if data_object.type == 'invoice' or data_object.type == 'contact':

            bill_addr = {}
            if data_object.street:
                bill_addr.update({'Line1': data_object.street, })
            if data_object.street2:
                bill_addr.update({'Line2': data_object.street2, })
            if data_object.city:
                bill_addr.update({'City': data_object.city, })
            if data_object.country_id:
                if data_object.country_id.name:
                    bill_addr.update({'Country': data_object.country_id.name, })
            if data_object.state_id:
                if data_object.state_id.name:
                    bill_addr.update({'CountrySubDivisionCode': data_object.state_id.name, })
            if data_object.zip:
                bill_addr.update({'PostalCode': data_object.zip, })

            dict_billAddr['BillAddr'] = bill_addr
            # dict_billAddr['BillAddr'] = {'Line1': data_object.street,
            #                              'Line2': (data_object.street2 or ""),
            #                              'City': (data_object.city or ""),
            #                              'Country': data_object.country_id.name,                                                         'CountrySubDivisionCode': data_object.state_id.name,
            #                              'PostalCode': data_object.zip}

        if self.type == 'delivery':

            ship_addr = {}
            if data_object.street:
                ship_addr.update({'Line1': data_object.street, })
            if data_object.street2:
                ship_addr.update({'Line2': data_object.street2, })
            if data_object.city:
                ship_addr.update({'City': data_object.city, })
            if data_object.country_id:
                if data_object.country_id.name:
                    ship_addr.update({'Country': data_object.country_id.name, })
            if data_object.state_id:
                if data_object.state_id.name:
                    ship_addr.update({'CountrySubDivisionCode': data_object.state_id.name, })
            if data_object.zip:
                ship_addr.update({'PostalCode': data_object.zip, })

            dict_shipAddr['ShipAddr'] = ship_addr
            # dict_shipAddr['ShipAddr'] = {'Line1': data_object.street, 'Line2': data_object.street2, 'City': data_object.city,
            #                              'Country': data_object.country_id.name, 'CountrySubDivisionCode': data_object.state_id.name,
            #                              'PostalCode': data_object.zip}

        dict.update(dict_email)
        dict.update(dict_phone)
        dict.update(dict_billAddr)
        dict.update(dict_shipAddr)

        if customer_id_retrieved and record_type and record_type == "indv_company":
            dict_parent_ref['ParentRef'] = {'value': str(customer_id_retrieved)}
            dict.update(dict_parent_ref)

            dict['Job'] = 'true'

        if is_update and customer_id_retrieved:
            dict['Id'] = str(customer_id_retrieved)
            dict['sparse'] = "true"

            ''' Check SyncToken '''
            if sync_token:
                dict['SyncToken'] = str(sync_token)
            result = self.sendDataToQuickbooksForUpdate(dict)
        else:
            if self.customer_rank:
                result = self.sendDataToQuickbook(dict)
            if self.supplier_rank:
                result = self.sendVendorDataToQuickbook(dict)

        if result:
            if is_update:
                _logger.info("UPDATED !!!!!!!!!!!!!!")
            else:
                _logger.info("EXPORTED !!!!!!!!!")
            return result
        else:
            _logger.info("ERROR WHILE UPLOADING !!!!!!!!!")

            return False

    def prepareVendorDictStructure(self, obj=False, record_type=False, vendor_id_retrieved=False, is_update=False,
                             sync_token=False):
        data_object = None

        if obj:
            data_object = obj
        else:
            data_object = self

        ''' This Function Exports Record to Quickbooks '''
        dict = {}
        dict_phone = {}
        dict_email = {}
        dict_mobile = {}
        dict_billAddr = {}
        dict_shipAddr = {}
        dict_parent_ref = {}
        dict_job = {}

        if data_object.mobile:
            dict['Mobile'] = {'FreeFormNumber': str(data_object.mobile)}

        if data_object.website:
            dict['WebAddr'] = {'URI': str(data_object.website)}

        if data_object.comment:
            dict["Notes"] = data_object.comment
        #
        # if data_object.name:
        #     dict["GivenName"] = str(data_object.name)
        #     dict['DisplayName'] = str(data_object.display_name)

        if data_object.name:
            full_name = str(data_object.name)
            if len(full_name.split()) == 1:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = " "
                dict["FamilyName"] = " "
            if len(full_name.split()) == 2:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = " "
                dict["FamilyName"] = full_name.split()[1]

            if len(full_name.split()) == 3:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = full_name.split()[1]
                dict["FamilyName"] = full_name.split()[2]

            dict['DisplayName'] = str(data_object.name)
            dict['PrintOnCheckName'] = str(data_object.name)

        if data_object.title:
            dict["Title"] = data_object.title.name

        if data_object.email:
            dict_email["PrimaryEmailAddr"] = {'Address': str(data_object.email)}

        if data_object.phone:
            dict_phone["PrimaryPhone"] = {'FreeFormNumber': str(data_object.phone)}

        if data_object.type == 'invoice' or data_object.type == 'contact':
            bill_addr = {}
            if data_object.street:
                bill_addr.update({'Line1': data_object.street,})
            if data_object.street2:
                bill_addr.update({'Line2': data_object.street2,})
            if data_object.city:
                bill_addr.update({'City': data_object.city,})
            if data_object.country_id:
               if data_object.country_id.name:
                   bill_addr.update({'Country': data_object.country_id.name,})
            if data_object.state_id:
                if data_object.state_id.name:
                    bill_addr.update({'CountrySubDivisionCode': data_object.state_id.name, })
            if data_object.zip:
                bill_addr.update({'PostalCode': data_object.zip, })
            dict_billAddr['BillAddr'] = bill_addr
            # dict_billAddr['BillAddr'] = {'Line1': data_object.street, 'Line2': (data_object.street2 or ""),
            #                              'City': (data_object.city or ""),
            #                              'Country': data_object.country_id.name,
            #                              'CountrySubDivisionCode': data_object.state_id.name,
            #                              'PostalCode': data_object.zip}

        if self.type == 'delivery':

            ship_addr = {}
            if data_object.street:
                ship_addr.update({'Line1': data_object.street, })
            if data_object.street2:
                ship_addr.update({'Line2': data_object.street2, })
            if data_object.city:
                ship_addr.update({'City': data_object.city, })
            if data_object.country_id:
                if data_object.country_id.name:
                    ship_addr.update({'Country': data_object.country_id.name, })
            if data_object.state_id:
                if data_object.state_id.name:
                    ship_addr.update({'CountrySubDivisionCode': data_object.state_id.name, })
            if data_object.zip:
                ship_addr.update({'PostalCode': data_object.zip, })
            dict_shipAddr['ShipAddr'] = ship_addr
            # dict_shipAddr['ShipAddr'] = {'Line1': data_object.street, 'Line2': data_object.street2,
            #                              'City': data_object.city,
            #                              'Country': data_object.country_id.name,
            #                              'CountrySubDivisionCode': data_object.state_id.name,
            #                              'PostalCode': data_object.zip}

        dict.update(dict_email)
        dict.update(dict_phone)
        dict.update(dict_billAddr)
        dict.update(dict_shipAddr)

        # if vendor_id_retrieved and record_type and record_type == "indv_company":
        #     dict_parent_ref['ParentRef'] = {'value': str(vendor_id_retrieved)}
        #     dict.update(dict_parent_ref)
        #
        #     dict['Job'] = 'true'

        if is_update and vendor_id_retrieved:

            dict['Id'] = str(vendor_id_retrieved)
            dict['sparse'] = "true"

            ''' Check SyncToken '''
            if sync_token:
                dict['SyncToken'] = str(sync_token)
            result = self.sendVendorDataToQuickbooksForUpdate(dict)
        else:
            result = self.sendVendorDataToQuickbook(dict)

        if result:
            if is_update:
                _logger.info("UPDATED !!!!!!!!!!!!!!")
            else:
                _logger.info("EXPORTED !!!!!!!!!!!!!!")
            return result
        else:
            _logger.info("ERROR WHILE UPLOADING !!!!!!!!!!!!!!")

            return False

    def updateExistingCustomer(self):
        ''' Check first if qbo_customer_id exists in quickbooks or not'''
        if self.x_quickbooks_exported or self.qbo_customer_id:
            ''' Hit request ot quickbooks and check response '''
            company = self.env['res.users'].search([('id', '=', 2)]).company_id

            ''' GET ACCESS TOKEN '''

            access_token = None
            realmId = None
            if company.access_token:
                access_token = company.access_token
            if company.id:
                realmId = company.realm_id

            if access_token:
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(access_token)
                headers['Content-Type'] = 'application/json'
                headers['Accept'] = 'application/json'

                sql_query = "select Id,SyncToken from customer Where Id = '{}'".format(str(self.qbo_customer_id))

                result = requests.request('GET', company.url + str(realmId) + "/query?query=" + sql_query, headers=headers)
                if result.status_code == 200:
                    parsed_result = result.json()

                    if parsed_result.get('QueryResponse') and parsed_result.get('QueryResponse').get('Customer'):
                        customer_id_retrieved = parsed_result.get('QueryResponse').get('Customer')[0].get('Id')
                        if customer_id_retrieved:
                            ''' HIT UPDATE REQUEST '''
                            syncToken = parsed_result.get('QueryResponse').get('Customer')[0].get('SyncToken')
                            result = self.prepareDictStructure(is_update=True, customer_id_retrieved=customer_id_retrieved, sync_token=syncToken)
                            if result:
                                return result
                            else:
                                return False
                else:
                    return False

    def updateExistingVendor(self):
        ''' Check first if qbo_customer_id exists in quickbooks or not'''
        if self.x_quickbooks_exported or self.qbo_vendor_id:
            ''' Hit request ot quickbooks and check response '''
            company = self.env['res.users'].search([('id', '=', 2)]).company_id

            ''' GET ACCESS TOKEN '''

            access_token = None
            realmId = None
            if company.access_token:
                access_token = company.access_token
            if company.id:
                realmId = company.realm_id

            if access_token:
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(access_token)
                headers['Content-Type'] = 'application/json'
                headers['Accept'] = 'application/json'

                sql_query = "select Id,SyncToken from vendor Where Id = '{}'".format(str(self.qbo_vendor_id))

                result = requests.request('GET', company.url + str(realmId) + "/query?query=" + sql_query, headers=headers)
                if result.status_code == 200:
                    parsed_result = result.json()

                    if parsed_result.get('QueryResponse') and parsed_result.get('QueryResponse').get('Vendor'):
                        vendor_id_retrieved = parsed_result.get('QueryResponse').get('Vendor')[0].get('Id')
                        if vendor_id_retrieved:
                            ''' HIT UPDATE REQUEST '''
                            syncToken = parsed_result.get('QueryResponse').get('Vendor')[0].get('SyncToken')
                            result = self.prepareVendorDictStructure(is_update=True, vendor_id_retrieved=vendor_id_retrieved, sync_token=syncToken)
                            if result:
                                return result
                            else:
                                return False
                else:
                    return False

    def createParentInQuickbooks(self, odoo_partner_object, company):
        ''' This Function Creates a new record in quicbooks and returns its Id
        For attaching with the record of customer which will be created in exportPartner Function'''

        if odoo_partner_object and company:

            result = self.prepareDictStructure(odoo_partner_object, record_type="company")
            if result:
                return result
        else:
            return False

    '''STEP 1 : Retrieve All Data from odoo_partner_object to form a dictionary which will be passed
            to Quickbooks'''
    def checkPartnerInQuickbooks(self, odoo_partner_object):
        ''' Check This Name in Quickbooks '''
        customer_id_retrieved = None
        company = self.env['res.users'].search([('id', '=', 2)]).company_id

        if company:

            access_token = None
            realmId = None
            if company.access_token:
                access_token = company.access_token
            if company.realm_id:
                realmId = company.realm_id

            if access_token and realmId:
                ''' Hit Quickbooks and Check Availability '''
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(access_token)
                headers['Content-Type'] = 'application/json'
                headers['Accept'] = 'application/json'

                if odoo_partner_object.supplier_rank:
                    sql_vendor_query = "select Id from vendor Where DisplayName = '{}'".format(
                        str(odoo_partner_object.name))
                    vendor_result = requests.request('GET',
                                                     company.url + str(realmId) + "/query?query=" + sql_vendor_query,
                                                     headers=headers)
                    if vendor_result.status_code == 200:
                        parsed_result = vendor_result.json()
                        if parsed_result.get('QueryResponse') and parsed_result.get('QueryResponse').get('Vendor'):
                            vendor_id_retrieved = parsed_result.get('QueryResponse').get('Vendor')[0].get('Id')
                            if vendor_id_retrieved:
                                return vendor_id_retrieved

                sql_query = "select Id from customer Where DisplayName = '{}'".format(str(odoo_partner_object.name))

                result = requests.request('GET', company.url + str(realmId) + "/query?query=" + sql_query,
                                          headers=headers)

                if result.status_code == 200:
                    parsed_result = result.json()

                    if parsed_result.get('QueryResponse') and parsed_result.get('QueryResponse').get('Customer'):
                        customer_id_retrieved = parsed_result.get('QueryResponse').get('Customer')[0].get('Id')
                        if customer_id_retrieved:
                            return customer_id_retrieved
                    if not parsed_result.get('QueryResponse').get('Customer'):
                        new_quickbooks_parent_id = self.createParentInQuickbooks(odoo_partner_object, company)
                        if new_quickbooks_parent_id:
                            if odoo_partner_object.customer:
                                odoo_partner_object.qbo_customer_id = new_quickbooks_parent_id
                            if odoo_partner_object.supplier_rank:
                                odoo_partner_object.qbo_vendor_id = new_quickbooks_parent_id
                            odoo_partner_object.x_quickbooks_exported = True

                            return new_quickbooks_parent_id
                        else:
                            _logger.info("Inside Else of new_quickbooks_parent_id !!!!!!!!!!!!!!")

                        return False
                else:
                    raise UserError("Error Occured In Partner Search Request" + result.text)
                return False
        else:
            _logger.info("Didnt Got QUickbooks Config !!!!!!!!!!!!!!")

    @api.model
    def exportCustomer(self):
        # print("CUSTOMER ---------", self)
        if self.x_quickbooks_exported or self.qbo_customer_id:

            # if self.qbo_customer_id:
            '''  If Customer Already Exported to quickbooks then hit update request '''

            # STEP 1 : GET ID FROM QUICKBOOKS USING GET REQUEST QUERY TO QUICKBOOKS
            update_customer = self.env['ir.config_parameter'].sudo().get_param('pragmatic_quickbooks_connector.update_customer_export')
            if update_customer:
                result = self.updateExistingCustomer()
                if result:
                    _logger.info("Update was successful !")
                    # raise UserError("Update was successful !")
                else:
                    _logger.info("Update was not successful !")
                    # raise UserError("Update unsuccessful :(")
            else:
                _logger.info("Your not allowed to update any customers while exporting. !")
        else:
            #             raise UserError("Customer Already Exported To Quickbooks")
            #             return False
            ''' Checking if parent_id is assigned or not if not then first read that parent_id and check in
            Quickbooks if present if present then make sub customer else first create that company in Quickbooks and
            attach its reference.
            '''

            if self.parent_id:
                ''' Check self.parent_id.name in Quickbooks '''
                customer_id_retrieved = self.checkPartnerInQuickbooks(self.parent_id)
                if customer_id_retrieved:
                    result = self.prepareDictStructure(record_type="indv_company",
                                                       customer_id_retrieved=customer_id_retrieved)
                    if result:
                        self.qbo_customer_id = result
                        self.x_quickbooks_exported = True
                        self._cr.commit()
                else:
                    _logger.info("Customer ID was not retrieved")

            if not self.parent_id:
                result = self.prepareDictStructure(record_type="individual")
                if result:
                    self.qbo_customer_id = result
                    self.x_quickbooks_exported = True
                    self._cr.commit()

    @api.model
    def exportVendor(self):
        if self.x_quickbooks_exported or self.qbo_vendor_id:
            # if self.qbo_customer_id:
            '''  If Customer Already Exported to quickbooks then hit update request '''

            # STEP 1 : GET ID FROM QUICKBOOKS USING GET REQUEST QUERY TO QUICKBOOKS
            update_vendor = self.env['ir.config_parameter'].sudo().get_param(
                'pragmatic_quickbooks_connector.update_vendor_export')

            if update_vendor:
                result = self.updateExistingVendor()
                if result:
                    _logger.info("Update was successful !")
                    # raise UserError("Update was successful !")
                else:
                    _logger.info("Update was not successful !")
                    # raise UserError("Update unsuccessful :(")
            else:
                _logger.info("Your not allowed to update any vendors while exporting.")
        else:

            #             raise UserError("Customer Already Exported To Quickbooks")
            #             return False
            ''' Checking if parent_id is assigned or not if not then first read that parent_id and check in 
            Quickbooks if present if present then make sub customer else first create that company in Quickbooks and 
            attach its reference.
            '''

            if self.parent_id:
                ''' Check self.parent_id.name in Quickbooks '''
                customer_id_retrieved = self.checkPartnerInQuickbooks(self.parent_id)
                if customer_id_retrieved:
                    result = self.prepareVendorDictStructure(record_type="indv_company",
                                                             vendor_id_retrieved=customer_id_retrieved)

                    if result:
                        self.qbo_vendor_id = result
                        self.x_quickbooks_exported = True
                        self._cr.commit()
                else:
                    _logger.info("Customer ID was not retrieved")


            if not self.parent_id:
                result = self.prepareVendorDictStructure(record_type="individual")
                if result:
                    self.qbo_vendor_id = result
                    self.x_quickbooks_exported = True
                    self._cr.commit()

    # @api.multi
    def export_single_Partner(self,partner):
        if partner.customer_rank:
            partner.exportCustomer()
        elif partner.supplier_rank == 1:
            partner.exportVendor()

    @api.model
    def exportPartner(self):

        # if len(self) > 1:
        #     raise UserError("Select 1 record at a time.")
        #     return
        if len(self) > 1:
            for customer in self:
                if customer.type == 'contact':
                    if customer.customer == True:
                        customer.exportCustomer()
                    elif customer.supplier_rank == 1:
                        customer.exportVendor()
        else:
            if self.type == 'contact':
                if self.customer_rank:
                    self.exportCustomer()
                elif self.supplier_rank:
                    self.exportVendor()