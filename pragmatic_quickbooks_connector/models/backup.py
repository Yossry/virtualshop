from odoo import api, fields, models, _
import requests
import json
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_vendor(self, data, is_customer=False, is_vendor=False):
        """Create partner object in odoo
        :param data: partner object response return by QBO
        :param is_customer: True if partner is a customer
        :param is_vendor: True if partener is a supplier/vendor
        :return int: last import QBO customer or vendor Id
        """
        res = json.loads(str(data.text))
        brw_partner = False
        if is_vendor:
            if 'QueryResponse' in res:
                partners = res.get('QueryResponse').get('Vendor', [])
            else:
                partners = [res.get('Vendor')] or []
        else:
            partners = []

        for partner in partners:
            vals = self._prepare_partner_dict(partner, is_customer=is_customer, is_vendor=is_vendor)
            brw_partner = self.search([('qbo_vendor_id', '=', partner.get('Id'))], limit=1)
            if not brw_partner:
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
                    # Create partner billing address
                    ship_addr = self.create(address_vals)
                _logger.info(_("Vendor created sucessfully! Partner Id: %s" % (brw_partner.id)))

            else:
                update_vendor = self.env['ir.config_parameter'].sudo().get_param(
                    'pragmatic_quickbooks_connector.update_vendor_import')
                if update_vendor:
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

                    _logger.info(_("Vendor updated sucessfully! Partner Id: %s" % (brw_partner.id)))
        return brw_partner

class Respartnercustomization(models.Model):
    _inherit = "res.partner"

    x_quickbooks_exported = fields.Boolean("Exported to Quickbooks ? ", copy=False, default=False)
    x_quickbooks_updated = fields.Boolean("Updated in Quickbook ?", copy=False, default=False)