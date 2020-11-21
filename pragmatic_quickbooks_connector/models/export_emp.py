from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
# from openerp.exceptions import UserError, ValidationError
import requests
import json
import logging
import datetime

_logger = logging.getLogger(__name__)

class Employee(models.Model):
    _inherit = "hr.employee"

    def getSyncToken(self, qbo_id):
        '''

        :param: Employee ID of quickbooks

        :return: Sync Token if found else False
        '''
        access_token_obj = self.env['res.users'].search([('id', '=', 2)]).company_id


        access_token = None
        realmId = None

        if access_token_obj.access_token:
            access_token = access_token_obj.access_token

        if access_token_obj.realm_id:
            realmId = access_token_obj.realm_id

        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

            sql_query = "select Id,SyncToken from employee Where Id = '{}'".format(str(qbo_id))

            result = requests.request('GET', access_token_obj.url + str(realmId) + "/query?query=" + sql_query,
                                      headers=headers)
            if result.status_code == 200:
                parsed_result = result.json()
                # print("PARSED RESULT !!!!", parsed_result)

                if parsed_result.get('QueryResponse') and parsed_result.get('QueryResponse').get('Employee'):
                    synctoken_id_retrieved = parsed_result.get('QueryResponse').get('Employee')[0].get('Id')
                    if synctoken_id_retrieved:
                        ''' HIT UPDATE REQUEST '''
                        syncToken = parsed_result.get('QueryResponse').get('Employee')[0].get('SyncToken')

                        if syncToken:
                            return syncToken
                        else:
                            return False

    def createEmployee(self):
        ''' This Function Exports Record to Quickbooks '''

        ''' STEP 3 '''

        # print("-------------------------------------------")

        ''' GET ACCESS TOKEN FROM RES COMPANY'''
        access_token_obj = self.env['res.users'].search([('id', '=', 2)]).company_id


        access_token = None
        realmId = None

        if access_token_obj.access_token:
            access_token = access_token_obj.access_token

        if access_token_obj.realm_id:
            realmId = access_token_obj.realm_id

        # print("<----------TOKEN--------->", access_token_obj)
        if access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(access_token)
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'
            # print("Header : ", headers)

        dict = {}
        dict_phone = {}
        dict_email = {}
        dict_work_phone = {}
        dict_addr = {}
        dict_birth = {}
        dict_eno = {}
        dict_gender = {}
        dict_id = {}
        dict_hired = {}
        dict_released = {}

        if self.work_phone:
            dict_work_phone['Mobile'] = {'FreeFormNumber': str(self.work_phone)}
            # print("Mobile : ", dict_work_phone['Mobile'])

        if self.gender:
            if self.gender == 'female':
                dict_gender['Gender'] = 'Female'
            if self.gender == 'male':
                dict_gender['Gender'] = 'Male'
            if self.gender == 'other':
                dict_gender['Gender'] = 'Other'
            # print("Gender : ", dict_gender['Gender'])

        if self.quickbook_id:
            dict["Id"] = self.quickbook_id
            dict['sparse'] = "true"
            # print("Id : ", dict["Id"])

        if self.ssn:
            dict["SSN"] = str(self.ssn)
            # print("SSN : ", dict["SSN"])

        if self.billing_rate:
            dict["BillRate"] = str(self.billing_rate)
            # print("BillRate : ", dict["BillRate"])

        if self.sync_id:
            dict["SyncToken"] = str(self.sync_id)
            # print("SyncToken : ", dict["SyncToken"])

        if self.employee_no:
            dict_id["EmployeeNumber"] = str(self.employee_no)
            # print("EmployeeNumber : ", dict_id["EmployeeNumber"])

        # if self.notes:
        #     dict["Notes"] = self.notes
        #     print("Notes : ",dict["Notes"])

        if self.name:
            full_name = str(self.name)
            if len(full_name.split()) == 1:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = "NA"
                dict["FamilyName"] = "NA"
            if len(full_name.split()) == 2:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = " "
                dict["FamilyName"] = full_name.split()[1]

            if len(full_name.split()) == 3:
                dict["GivenName"] = full_name.split()[0]
                dict["MiddleName"] = full_name.split()[1]
                dict["FamilyName"] = full_name.split()[2]

            dict['DisplayName'] = str(self.name)
            dict['PrintOnCheckName'] = str(self.name)

            # print("Name : ", dict["GivenName"])

        if self.birthday:
            dict_birth["BirthDate"] = self.birthday
            # print("BDAY : ", dict_birth["BirthDate"])

        if self.released_date:
            dict_released["ReleasedDate"] = str(self.released_date)
            # print("Released Date : ", dict_released["ReleasedDate"])

        if self.hired_date:
            dict_hired["HiredDate"] = str(self.hired_date)
            # print("Hired Date: ", dict_hired["HiredDate"])

        if self.work_email:
            dict_email["PrimaryEmailAddr"] = {'Address': str(self.work_email)}
            # print("Email : ", dict_email["PrimaryEmailAddr"])

        if self.mobile_phone:
            dict_phone["PrimaryPhone"] = {'FreeFormNumber': str(self.mobile_phone)}

        res_partner = self.env['res.partner'].search([('id', '=', self.address_id.id)], limit=1)

        # print("res_partner : ", res_partner)

        if self.address_id:
            dict_addr['PrimaryAddr'] = {'Line1': (res_partner.street or ""), 'Line2': (res_partner.street2 or ""),
                                        'City': (res_partner.city or ""),
                                        'Country': (res_partner.country_id.name or ""),
                                        'CountrySubDivisionCode': (res_partner.state_id.name or ""),
                                        'PostalCode': (res_partner.zip or "")}

        # else:
        #     if self.work_location:
        #         dict_addr['PrimaryAddr'] = {'City': (self.work_location)}

        dict.update(dict_email)
        dict.update(dict_id)
        dict.update(dict_gender)
        dict.update(dict_work_phone)
        dict.update(dict_phone)
        dict.update(dict_eno)
        dict.update(dict_birth)
        dict.update(dict_hired)
        dict.update(dict_released)
        dict.update(dict_addr)

        # print("SyncToken from dict : ", self.sync_id)
        if self.quickbook_id:

            dict["SyncToken"] = str(self.sync_id)

            res = self.getSyncToken(self.quickbook_id)
            if res:
                dict["SyncToken"] = str(res)
                # print("SYNC TOKEN WAS SET", dict['SyncToken'])

                # print("DICT GOING FOR POST", dict)
                parsed_dict = json.dumps(dict)
                result_data = requests.request('POST',
                                               access_token_obj.url + str(realmId) + "/employee?operation=update",
                                               headers=headers, data=parsed_dict)
                # print("Updated Result : ", result_data)
                if result_data.status_code == 200:
                    parsed_result = result_data.json()

                    if parsed_result.get('Employee').get('Id'):
                        # print("SUCCESS !!!!!! UPDATED !!!!!!!!!", parsed_result.get('Employee').get('Id'))

                        return parsed_result.get('Employee').get('Id')
                    else:
                        return False

                else:
                    raise UserError("Error Occured While Updating" + result_data.text)
                    return False


        else:
            parsed_dict = json.dumps(dict)
            # print("\n\n---- dict ---",parsed_dict)
            result_data = requests.request('POST', access_token_obj.url + str(realmId) + "/employee", headers=headers,
                                           data=parsed_dict)
            if result_data.status_code == 200:

                parsed_result = result_data.json()
                # print("PARSED RESULT : ", parsed_result)

                if parsed_result.get('Employee').get('Id'):
                    # print("SUCCESS !!!!!!")
                    dict_c = {}
                    if parsed_result.get('Employee').get('Id'):
                        dict_c['quickbook_id'] = parsed_result.get('Employee').get('Id')

                    if parsed_result.get('Employee').get('SyncToken'):
                        dict_c['sync_id'] = parsed_result.get('Employee').get('SyncToken')

                    return dict_c['quickbook_id']

                    # return parsed_result.get('Employee').get('Id')
                else:
                    return False
            else:
                # print("Something went wrong")
                raise UserError("Error Occured While Exporting" + result_data.text)
                return False

    @api.model
    def exportEmployee(self):
        ''' This Function call the function that Exports Record to Quickbooks and updates quickbook_id'''

        ''' STEP 2 '''

        # print("Inside Create !!!!!!!!!!!!!!!!!!!", self)

        result = self.createEmployee()
        # print("Inside Create !!!!!!!!!!!!!!!!!!!", type(result),self)
        if result:

            self.write({

                'quickbook_id': int(result)

            })
        else:
            raise Warning("Oops Some error occured.")
            # raise UserError("Creation was successful !")

    @api.model
    def export_Employees_to_qbo(self):
        '''First function that is called from Export to QB action button'''

        ''' STEP 1 '''

        if len(self) > 1:

            '''For more then one employees'''
            for i in self:
                # print("Id from for : ", i)
                i.exportEmployee()
                # print("Ids --------------- > ", i.id)
        else:

            '''For only one employee'''
            self.exportEmployee()

