from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
# from openerp.exceptions import UserError, ValidationError
import requests
import json
import logging
import datetime

_logger = logging.getLogger(__name__)

class Dept(models.Model):
    _inherit = "hr.department"

    @api.model
    def _prepare_dept_export_dict(self):
        vals = {}
        # print("Parent id ---------->",self.parent_id)
        # parent = self.env['hr.department'].search(['id','=',self.parent_id])
        # print("parent =====> ",parent)
        if self.name:
            vals.update({
                            'Name': self.name,
                        })
        if self.parent_id:
            vals.update({
                            'ParentRef': {
                                'value': self.env['hr.department'].get_qbo_dept_ref(self.parent_id)
                            }
                        })
        return vals

    @api.model
    def exportDepartment(self):
        """export account invoice to QBO"""
        quickbook_config = self.env['res.users'].search([('id', '=', 2)]).company_id

        if self._context.get('active_ids'):
            dept = self.browse(self._context.get('active_ids'))
        else:
            dept = self

        for d in dept:
            if d.quickbook_id:
                vals = d._prepare_dept_export_dict()
                parsed_dict = json.dumps(vals)
                if quickbook_config.access_token:
                    access_token = quickbook_config.access_token
                if quickbook_config.realm_id:
                    realmId = quickbook_config.realm_id

                if access_token:
                    # print("<-------------------->")
                    headers = {}
                    headers['Authorization'] = 'Bearer ' + str(access_token)
                    headers['Content-Type'] = 'application/json'

                    result = requests.request('POST', quickbook_config.url + str(realmId) + "/department?operation=update",
                                              headers=headers, data=parsed_dict)
                    # print("RESULT ----------> ",result)
                    if result.status_code == 200:
                        response = quickbook_config.convert_xmltodict(result.text)
                        # print("RESPONSE : ---------------/> ", response)
                        # update QBO invoice id
                        if d.name:
                            d.quickbook_id = response.get('IntuitResponse').get('Department').get('Id')
                            self._cr.commit()
                        _logger.info(_("exported successfully to QBO"))
                    #                         return True
                    else:
                        _logger.info(_("NO CHANGES IN DEPT"))
                        # _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                        # raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))
            else:
                vals = d._prepare_dept_export_dict()
                parsed_dict = json.dumps(vals)
                if quickbook_config.access_token:
                    access_token = quickbook_config.access_token
                if quickbook_config.realm_id:
                    realmId = quickbook_config.realm_id

                if access_token:
                    headers = {}
                    headers['Authorization'] = 'Bearer ' + str(access_token)
                    headers['Content-Type'] = 'application/json'

                    result = requests.request('POST', quickbook_config.url + str(realmId) + "/department",
                                              headers=headers, data=parsed_dict)

                    if result.status_code == 200:
                        response = quickbook_config.convert_xmltodict(result.text)
                        # print("RESPONSE : ---------------/> ",response)
                        # update QBO invoice id
                        if d.name:
                            d.quickbook_id = response.get('IntuitResponse').get('Department').get('Id')
                            self._cr.commit()
                        _logger.info(_("exported successfully to QBO"))
                    #                         return True
                    else:
                        _logger.error(_("[%s] %s" % (result.status_code, result.reason)))
                        raise ValidationError(_("[%s] %s %s" % (result.status_code, result.reason, result.text)))
