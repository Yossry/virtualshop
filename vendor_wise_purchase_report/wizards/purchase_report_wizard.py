from odoo import models, fields, api, _


class PurchaseReportVendor(models.TransientModel):
    _name = 'vendor.purchase.report.wizard'

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    state = fields.Selection([('draft', 'RFQ'), ('sent', 'Sent RFQ'), ('purchase', 'Purchase Order'), ('done', 'Done'),
                              ('cancel', 'Cancelled'), ], string="Status")
    vendor_ids = fields.Many2many('res.partner', string='Vendors', required=True)

    def print_vendor_wise_purchase_report(self):
        purchase_order = self.env['purchase.order'].search([])
        purchase_order_groupby_dict = {}
        for vendor in self.vendor_ids:
            filtered_purchase_order = list(filter(lambda x: x.partner_id == vendor, purchase_order))
            print('filtered_sale_order ===', filtered_purchase_order)
            filtered_by_date = list(filter(lambda x: x.date_order >= self.start_date and x.date_order <= self.end_date,
                                           filtered_purchase_order))
            print('State:', self.state)
            filtered_by_state = list(filter(lambda x: x.state == self.state or self.state == False, filtered_by_date))

            purchase_order_groupby_dict[vendor.name] = filtered_by_state

        final_dist = {}
        for vendor in purchase_order_groupby_dict.keys():
            purchase_data = []
            for order in purchase_order_groupby_dict[vendor]:

                order_state = self.get_state_display_value(order.state)

                temp_data = []
                temp_data.append(order.name)
                temp_data.append(order.date_order)
                temp_data.append(order.user_id.name)
                temp_data.append(order_state)
                temp_data.append(order.amount_total)
                purchase_data.append(temp_data)
            final_dist[vendor] = purchase_data
        datas = {
            'ids': self,
            'model': 'vendor.purchase.report.wizard',
            'form': final_dist,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

        print('datas:', datas)
        return self.env.ref('vendor_wise_purchase_report.report_purchase_vendor').report_action([], data=datas)

    def get_state_display_value(self, order_state):
        if order_state == 'draft':
            order_state = 'RFQ'
        elif order_state == 'purchase':
            order_state = 'Purchase Order'
        elif order_state == 'sent':
            order_state = 'RFQ Sent'
        elif order_state == 'done':
            order_state = 'Done'
        elif order_state == 'cancel':
            order_state = 'Cancelled'
        return order_state