# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import ValidationError


class ProductSalesReportWeekly(models.AbstractModel):
    _name = 'report.product_sales_report.report_of_product_sales_weekly_view'
    _description = 'Product Sales Report Weekly'

    def create_dict(self, report_of, qty, line, pro_dict, day_order):
        if report_of == 'product':
            obj_id = line.product_id.id
            obj_name = line.product_id.display_name
        if report_of == 'category':
            obj_id = line.product_id.categ_id.id
            obj_name = line.product_id.categ_id.name
        if obj_id not in pro_dict:
            pro_dict.update(
                {obj_id: {'Name': obj_name, 'Qty': [0, 0, 0, 0, 0, 0, 0]}})
        pro_dict[obj_id]['Qty'][day_order] += qty

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'product_sales_report.report_of_product_sales_weekly_view')

        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']

        user_team_dict = {}
        if data['report_by'] == 'sales_team':
            if not data['team_id']:
                data['team_id'] = self.env['crm.team'].search([]).ids
            for team in data['team_id']:
                team_id = self.env['crm.team'].browse(team)
                team_domain = data['sale_domain'] + [('team_id', '=', team)]
                order_ids = self.env['sale.order'].search(team_domain)
                days_dict_prodct = {}
                for order_id in order_ids:
                    day_order = order_id.date_order.weekday()
                    for line_id in order_id.order_line:
                        self.create_dict(
                            data['report_of'], line_id.product_uom_qty,
                            line_id, days_dict_prodct, day_order)

                if data['pos_domain']:
                    team_domain = data['pos_domain'] + \
                        [('config_id.crm_team_id', '=', team)]
                    order_ids = self.env['pos.order'].search(team_domain)
                    for order_id in order_ids:
                        day_order = order_id.date_order.weekday()
                        for line in order_id.lines:
                            self.create_dict(
                                data['report_of'], line.qty, line,
                                days_dict_prodct, day_order)

                if days_dict_prodct:
                    user_team_dict.update({team_id.name: days_dict_prodct})

        if data['report_by'] == 'sales_person':
            if not data['user_id']:
                data['user_id'] = self.env['res.users'].search([]).ids
            for user in data['user_id']:
                user_id = self.env['res.users'].browse(user)
                user_domain = data['sale_domain'] + [('user_id', '=', user)]
                order_ids = self.env['sale.order'].search(user_domain)
                days_dict_prodct = {}
                for order_id in order_ids:
                    day_order = order_id.date_order.weekday()
                    for line_id in order_id.order_line:
                        self.create_dict(
                            data['report_of'], line_id.product_uom_qty,
                            line_id, days_dict_prodct, day_order)

                if data['pos_domain']:
                    user_domain = data['pos_domain'] + [('user_id', '=', user)]
                    order_ids = self.env['pos.order'].search(user_domain)
                    for order_id in order_ids:
                        day_order = order_id.date_order.weekday()
                        for line in order_id.lines:
                            self.create_dict(
                                data['report_of'], line.qty, line,
                                days_dict_prodct, day_order)

                if days_dict_prodct:
                    user_team_dict.update({user_id.name: days_dict_prodct})

        if not user_team_dict:
            raise ValidationError("Record's Not Exist...")

        return {
            'doc_ids': user_team_dict,
            'doc_model': report.model,
            'header_list': ['Name', 'Qty'],
            'days': days,
            'data': data,
        }
