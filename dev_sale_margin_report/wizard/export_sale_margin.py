# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo.tools.misc import xlwt
from io import BytesIO
from odoo import api, fields, models, _
from xlwt import easyxf
import base64
from datetime import date, datetime


class ExportSaleMargin(models.TransientModel):
    _name ='export.sale.margin'

    def print_pdf_sale_margin(self):
        return self.env.ref('dev_sale_margin_report.menu_sale_margin_report').report_action(self)

    def get_margin_percentage(self, line):
        sale_price = discount = cost = margin_amount = margin_percentage = 0.0
        sale_price_after_discount = 0.0
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
        return round(margin_percentage,2)

    def export_sale_margin_report(self):
        filename = 'Sale Margin Report.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sale Margin Report')

        # defining various font styles
        header_style = easyxf('font:height 430;pattern: pattern solid, fore_color 0x3F; align: horiz center;font:bold True;')
        sub_header = easyxf('font:height 210;pattern: pattern solid, fore_color silver_ega;font:bold True;align: horiz center;')
        content = easyxf('font:height 200;')
        content_center = easyxf('font:height 200;align: horiz center;')
        content_center_red = easyxf('font:height 200;align: horiz center;font: colour red;')
        content_red = easyxf('font:height 200;font: colour red;')
        content_right = easyxf('font:height 200;align: horiz right;', num_format_str='0.00')
        content_right_red = easyxf('font:height 200;align: horiz right;font: colour red;', num_format_str='0.00')
        content_date2 = easyxf('font:height 200;align: horiz center;')

        # setting with of the column
        worksheet.col(0).width = 60 * 60
        worksheet.col(1).width = 60 * 60
        worksheet.col(2).width = 60 * 60
        worksheet.col(3).width = 60 * 60
        worksheet.col(4).width = 60 * 60
        worksheet.col(5).width = 60 * 60
        worksheet.col(6).width = 60 * 60
        worksheet.col(7).width = 60 * 60
        worksheet.col(8).width = 65 * 65
        worksheet.col(9).width = 60 * 60
        worksheet.col(10).width = 60 * 60
        worksheet.col(11).width = 60 * 60

        worksheet.write_merge(1, 3, 1, 4, 'Sale Margin Report', header_style)

        # writing (Labels)
        worksheet.write(5,1,'From ', content_right)
        start = datetime.strptime(str(self.start_date), '%Y-%m-%d')
        start_date = start.strftime('%d/%m/%Y')
        worksheet.write(5,2,start_date, content_date2)
        worksheet.write(5,4,'To ', content_right)
        end = datetime.strptime(str(self.end_date), '%Y-%m-%d')
        end_date = end.strftime('%d/%m/%Y')
        worksheet.write(5,5,end_date, content_date2)
        worksheet.write_merge(7, 8, 0, 0, 'Sale Order', sub_header)
        worksheet.write_merge(7, 8, 1, 1, 'Product', sub_header)
        worksheet.write_merge(7, 8, 2, 2, 'Order Date', sub_header)
        worksheet.write_merge(7, 8, 3, 3, 'Customer', sub_header)
        worksheet.write_merge(7, 8, 4, 4, 'Warehouse', sub_header)
        worksheet.write_merge(7, 8, 5, 5, 'Sale Team', sub_header)
        worksheet.write_merge(7, 8, 6, 6, 'Salesperson', sub_header)
        worksheet.write_merge(7, 8, 7, 7, 'Cost', sub_header)
        worksheet.write_merge(7,8,8,8,'Price\n(Tax Excluded)', sub_header)
        worksheet.write_merge(7, 8, 9, 9, 'Discount', sub_header)
        worksheet.write_merge(7, 8, 10, 10, 'Margin', sub_header)
        worksheet.write_merge(7, 8, 11, 11, 'Margin(%)', sub_header)

        # content writing

        domain = [('state', 'in', ['sale','done']),
                  ('date_order', '>=', self.start_date),
                  ('date_order', '<=', self.end_date)]

        if self.customer_ids:
            customer_domain = ('partner_id', 'in', self.customer_ids.ids)
            domain.append(customer_domain)
        if self.user_ids:
            user_domain = ('user_id', 'in', self.user_ids.ids)
            domain.append(user_domain)
        if self.warehouse_ids:
            warehouse_domain = ('warehouse_id', 'in', self.warehouse_ids.ids)
            domain.append(warehouse_domain)
        if self.sale_team_ids:
            team_domain = ('team_id', 'in', self.sale_team_ids.ids)
            domain.append(team_domain)
        if self.company_ids:
            company_domain = ('company_id', 'in', self.company_ids.ids)
            domain.append(company_domain)

        sale_order_ids = self.env['sale.order'].search(domain)

        row_counter = 9
        if sale_order_ids:
            for sale_id in sale_order_ids:
                if sale_id.order_line:
                    product_domain = self.product_ids.ids
                    for line in sale_id.order_line:
                        content_style = content
                        center_cell = content_center
                        if line.margin < 0 and self.highlight_negative_margin:
                            content_style = content_red
                            center_cell = content_center_red
                        decimal_right_content = content_right
                        if line.margin < 0 and self.highlight_negative_margin:
                            decimal_right_content = content_right_red
                        if not product_domain:
                            worksheet.write(row_counter, 0, sale_id.name or '',  center_cell)
                            worksheet.write(row_counter, 1, line.product_id.name or '',  content_style)
                            order_date = datetime.strptime(str(sale_id.date_order), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y')
                            worksheet.write(row_counter, 2, order_date or '',  center_cell)
                            worksheet.write(row_counter, 3, sale_id.partner_id.name or '',  content_style)
                            worksheet.write(row_counter, 4, sale_id.warehouse_id.name or '',  center_cell)
                            worksheet.write(row_counter, 5, sale_id.team_id.name or '',  center_cell)
                            worksheet.write(row_counter, 6, sale_id.user_id.name or '',  content_style)
                            worksheet.write(row_counter, 7, line.product_id.standard_price or 0,  decimal_right_content)
                            without_tax_price = line.price_unit * line.product_uom_qty
                            worksheet.write(row_counter, 8, without_tax_price or 0,  decimal_right_content)
                            sale_price = line.price_unit * line.product_uom_qty
                            discount_amount = (sale_price * line.discount) / 100
                            worksheet.write(row_counter, 9, discount_amount, decimal_right_content)
                            worksheet.write(row_counter, 10, line.margin, decimal_right_content)
                            margin_percentage = self.get_margin_percentage(line)
                            worksheet.write(row_counter, 11, margin_percentage,  decimal_right_content)
                            row_counter += 1
                        if product_domain:
                            if line.product_id.id in product_domain:
                                worksheet.write(row_counter, 0, sale_id.name or '', center_cell)
                                worksheet.write(row_counter, 1, line.product_id.name or '', content_style)
                                order_date = datetime.strptime(str(sale_id.date_order), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y')
                                worksheet.write(row_counter, 2, order_date or '', center_cell)
                                worksheet.write(row_counter, 3, sale_id.partner_id.name or '', content_style)
                                worksheet.write(row_counter, 4, sale_id.warehouse_id.name or '', center_cell)
                                worksheet.write(row_counter, 5, sale_id.team_id.name or '', center_cell)
                                worksheet.write(row_counter, 6, sale_id.user_id.name or '', content_style)
                                worksheet.write(row_counter, 7, line.product_id.standard_price or 0, decimal_right_content)
                                without_tax_price = line.price_unit * line.product_uom_qty
                                worksheet.write(row_counter, 8, without_tax_price or 0, decimal_right_content)
                                sale_price = line.price_unit * line.product_uom_qty
                                discount_amount = (sale_price * line.discount) / 100
                                worksheet.write(row_counter, 9, discount_amount, decimal_right_content)
                                worksheet.write(row_counter, 10, line.margin, decimal_right_content)
                                margin_percentage = self.get_margin_percentage(line)
                                worksheet.write(row_counter, 11, margin_percentage, decimal_right_content)
                                row_counter += 1

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})
        active_id = self.ids[0]
        url = ('web/content/?model=export.sale.margin&download=true&field=excel_file&id=%s&filename=%s' % (active_id, filename))
        if self.excel_file:
            return {'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'new'}

    start_date = fields.Date(string="From", default=date.today(), required=True)
    end_date = fields.Date(string="To", default=date.today(), required=True)
    excel_file = fields.Binary(string='Excel File')
    company_ids = fields.Many2many('res.company', string='Company')
    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouse')
    product_ids = fields.Many2many('product.product', string='Product')
    customer_ids = fields.Many2many('res.partner', string='Customer', domain=[('customer_rank', '=', 1)])
    sale_team_ids = fields.Many2many('crm.team', string='Sale Team')
    user_ids = fields.Many2many('res.users', string='Salesperson')
    highlight_negative_margin = fields.Boolean(string='Highlight Negative Margin')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: