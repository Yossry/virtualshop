from odoo import fields, models, api

class PurchaseReportVendor(models.AbstractModel):
    _name = 'report.vendor_wise_purchase_report.purchase_report_vendor'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }