# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, models
from datetime import datetime


class SaleMarginReport(models.AbstractModel):
    _name = 'report.dev_sale_margin_report.template_sale_margin_report'

    def get_date(self, base_date):
        date = datetime.strptime(str(base_date), '%Y-%m-%d')
        final_date = date.strftime('%d/%m/%Y')
        return final_date

    def get_margin_percentage(self, line):
        sale_price = discount = cost = margin_amount = margin_percentage = 0.0
        sale_price_after_discount = 0.0
        final_percentage = 0
        if line.product_id or line.margin_percentage:
            sale_price = line.price_unit * line.product_uom_qty
            discount = (sale_price*line.discount)/100
            cost = line.purchase_price * line.product_uom_qty
            margin_amount = (sale_price - discount) - cost
            sale_price_after_discount = sale_price - discount
            if discount:
                sale_price = sale_price_after_discount
            if cost and sale_price:
                margin_percentage = (margin_amount / sale_price) * 100
            else:
                margin_percentage = 100
        return round(margin_percentage, 2)

    def get_margin_data(self, wizard_id):
        margin_data = []
        domain = [('state', 'in', ['sale', 'done']),
                  ('date_order', '>=', wizard_id.start_date),
                  ('date_order', '<=', wizard_id.end_date)]

        if wizard_id.customer_ids:
            customer_domain = ('partner_id', 'in', wizard_id.customer_ids.ids)
            domain.append(customer_domain)
        if wizard_id.user_ids:
            user_domain = ('user_id', 'in', wizard_id.user_ids.ids)
            domain.append(user_domain)
        if wizard_id.warehouse_ids:
            warehouse_domain = ('warehouse_id', 'in', wizard_id.warehouse_ids.ids)
            domain.append(warehouse_domain)
        if wizard_id.sale_team_ids:
            team_domain = ('team_id', 'in', wizard_id.sale_team_ids.ids)
            domain.append(team_domain)
        if wizard_id.company_ids:
            company_domain = ('company_id', 'in', wizard_id.company_ids.ids)
            domain.append(company_domain)

        sale_order_ids = self.env['sale.order'].search(domain)

        if sale_order_ids:
            for sale_id in sale_order_ids:
                if sale_id.order_line:
                    product_domain = wizard_id.product_ids.ids
                    for line in sale_id.order_line:
                        if not product_domain:
                            red_line = False
                            if line.margin < 0 and wizard_id.highlight_negative_margin:
                                red_line = True
                            order_date = datetime.strptime(str(sale_id.date_order), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y')
                            without_tax_price = line.price_unit * line.product_uom_qty
                            sale_price = line.price_unit * line.product_uom_qty
                            discount_amount = (sale_price * line.discount) / 100
                            margin_percentage = self.get_margin_percentage(line)

                            data_dict = {'sale_order': sale_id.name or '',
                                         'product': line.product_id.name or '',
                                         'date': order_date,
                                         'customer': sale_id.partner_id.name or '',
                                         'warehouse': sale_id.warehouse_id.name or '',
                                         'team': sale_id.team_id.name or '',
                                         'salesperson': sale_id.user_id.name or '',
                                         'cost': ("%.2f" % line.product_id.standard_price or 0),
                                         'price': ("%.2f" % without_tax_price or 0),
                                         'discount': ("%.2f" % discount_amount or 0),
                                         'margin': ("%.2f" % line.margin or 0),
                                         'margin_percentage': ("%.2f" %  margin_percentage),
                                         'red_line': red_line
                                         }
                            margin_data.append(data_dict)
                        if product_domain:
                            if line.product_id.id in product_domain:
                                red_line = False
                                if line.margin < 0 and wizard_id.highlight_negative_margin:
                                    red_line = True
                                order_date = datetime.strptime(str(sale_id.date_order), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y')
                                without_tax_price = line.price_unit * line.product_uom_qty
                                sale_price = line.price_unit * line.product_uom_qty
                                discount_amount = (sale_price * line.discount) / 100
                                margin_percentage = self.get_margin_percentage(line)
                                data_dict = {'sale_order': sale_id.name or '',
                                             'product': line.product_id.name or '',
                                             'date': order_date,
                                             'customer': sale_id.partner_id.name or '',
                                             'warehouse': sale_id.warehouse_id.name or '',
                                             'team': sale_id.team_id.name or '',
                                             'salesperson': sale_id.user_id.name or '',
                                             'cost': ("%.2f" % line.product_id.standard_price or 0),
                                             'price': ("%.2f" % without_tax_price or 0),
                                             'discount': ("%.2f" % discount_amount or 0),
                                             'margin': ("%.2f" % line.margin or 0),
                                             'margin_percentage': margin_percentage or 0,
                                             'red_line': red_line
                                             }
                                margin_data.append(data_dict)
        return margin_data

    @api.model
    def _get_report_values(self, docids, data=None):
        records = self.env['export.sale.margin'].browse(docids)
        return {'doc_ids': records.ids,
                'doc_model': 'export.sale.margin',
                'docs': records,
                'data': data,
                'get_margin_data': self.get_margin_data,
                'get_margin_percentage': self.get_margin_percentage,
                'get_date': self.get_date
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: