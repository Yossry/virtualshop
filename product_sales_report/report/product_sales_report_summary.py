# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import ValidationError


class ProductSalesReportSummary(models.AbstractModel):
    _name = 'report.product_sales_report.report_of_product_sales_view'
    _description = 'Product Sales Report Summary'

    def create_dict(self, report_of, qty, currency, line, dict_prodct, dict_total, dict_final_total, currency_ids):
        if report_of == 'product':
            obj_id = line.product_id.id
            obj_name = line.product_id.display_name
        else:
            obj_id = line.product_id.categ_id.id
            obj_name = line.product_id.categ_id.name
        if obj_id not in dict_prodct:
            dict_prodct.update({obj_id: {'Name': obj_name, 'Quantity': 0.0}})
            for currency_id in currency_ids:
                dict_prodct[obj_id][currency_id.id] = {
                    'position': currency_id.position,
                    'symbol': currency_id.symbol, 'amount': 0}
        dict_prodct[obj_id]['Quantity'] += qty
        dict_prodct[obj_id][currency.id]['amount'] += line.price_unit
        dict_total[currency.id]['amount'] += line.price_unit
        dict_final_total[currency.id]['amount'] += line.price_unit

    def find_currency_set_dict(self, user_team, data, currency_ids, dict_final_total, header_list, currency_list):
        if data['pos_domain']:
            if data['report_by'] == 'sales_team':
                new_domain = data['pos_domain'] + \
                    [('config_id.crm_team_id', 'in', user_team)]
            else:
                new_domain = data['pos_domain'] + \
                    [('user_id', 'in', user_team)]
            pos_order = self.env['pos.order'].read_group(
                new_domain, ['pricelist_id'], ['pricelist_id'])
            for order in pos_order:
                pricelist = self.env['product.pricelist'].browse(
                    order.get('pricelist_id')[0])
                currency_ids.append(pricelist.currency_id)

        if data['report_by'] == 'sales_person':
            new_domain = data['sale_domain'] + [('user_id', 'in', user_team)]
        else:
            new_domain = data['sale_domain'] + [('team_id', 'in', user_team)]

        order_ids = self.env['sale.order'].search(new_domain)
        order_line = self.env['sale.order.line'].read_group([
            ('order_id', 'in', order_ids.ids)], ['currency_id'],
            ['currency_id'])
        for line in order_line:
            currency_id = self.env['res.currency'].browse(
                line.get('currency_id')[0])
            if currency_id not in currency_ids:
                currency_ids.append(currency_id)
        for currency in currency_ids:
            dict_final_total.update({currency.id: {
                'position': currency.position, 'symbol': currency.symbol,
                'amount': 0}})
            header_list.append(currency.id)
            currency_list.append(currency.name)

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'product_sales_report.report_of_product_sales_view')

        user_team_dict = {}
        dict_final_total = {}
        final_qty = 0.0
        currency_ids = []
        header_list = ['Name', 'Quantity']
        currency_list = []
        if data['report_by'] == 'sales_team':
            if not data['team_id']:
                data['team_id'] = self.env['crm.team'].search([]).ids

            self.find_currency_set_dict(
                data['team_id'], data, currency_ids, dict_final_total,
                header_list, currency_list)

            for team in data['team_id']:
                team_id = self.env['crm.team'].browse(team)
                team_domain = data['sale_domain'] + [('team_id', '=', team)]
                order_ids = self.env['sale.order'].search(team_domain)
                dict_product_total = {}
                for currency in currency_ids:
                    dict_product_total.update({currency.id: {
                        'position': currency.position,
                        'symbol': currency.symbol, 'amount': 0}})
                dict_prodct = {}
                total_qty = 0.0
                for order_id in order_ids:
                    for line_id in order_id.order_line:
                        total_qty += line_id.product_uom_qty
                        self.create_dict(
                            data['report_of'], line_id.product_uom_qty,
                            line_id.currency_id, line_id, dict_prodct,
                            dict_product_total, dict_final_total, currency_ids)

                if data['pos_domain']:
                    team_domain = data['pos_domain'] + \
                        [('config_id.crm_team_id', '=', team)]
                    order_ids = self.env['pos.order'].search(team_domain)
                    for order_id in order_ids:
                        currency = order_id.pricelist_id.currency_id
                        for line in order_id.lines:
                            total_qty += line.qty
                            self.create_dict(
                                data['report_of'], line.qty, currency, line,
                                dict_prodct, dict_product_total,
                                dict_final_total, currency_ids)

                if dict_prodct:
                    final_qty += total_qty
                    dict_product_total['Name'] = 'Total :'
                    dict_product_total['Quantity'] = total_qty
                    dict_prodct.update({team_id.name: dict_product_total})
                    user_team_dict.update({team_id.name: dict_prodct})

        if data['report_by'] == 'sales_person':
            if not data['user_id']:
                data['user_id'] = self.env['res.users'].search([]).ids

            self.find_currency_set_dict(
                data['user_id'], data, currency_ids, dict_final_total,
                header_list, currency_list)

            for user in data['user_id']:
                user_id = self.env['res.users'].browse(user)
                user_domain = data['sale_domain'] + [('user_id', '=', user)]
                order_ids = self.env['sale.order'].search(user_domain)
                dict_prodct = {}
                dict_product_total = {}
                for currency in currency_ids:
                    dict_product_total.update({currency.id: {
                        'position': currency.position,
                        'symbol': currency.symbol, 'amount': 0}})
                total_qty = 0
                for order_id in order_ids:
                    for line_id in order_id.order_line:
                        total_qty += line_id.product_uom_qty
                        self.create_dict(
                            data['report_of'], line_id.product_uom_qty,
                            line_id.currency_id, line_id, dict_prodct,
                            dict_product_total, dict_final_total, currency_ids)

                if data['pos_domain']:
                    user_domain = data['pos_domain'] + [('user_id', '=', user)]
                    order_ids = self.env['pos.order'].search(user_domain)
                    for order_id in order_ids:
                        currency = order_id.pricelist_id.currency_id
                        for line in order_id.lines:
                            total_qty += line.qty
                            self.create_dict(
                                data['report_of'], line.qty, currency, line,
                                dict_prodct, dict_product_total,
                                dict_final_total, currency_ids)

                if dict_prodct:
                    final_qty += total_qty
                    dict_product_total['Name'] = 'Total :'
                    dict_product_total['Quantity'] = total_qty
                    dict_prodct.update({user_id.name: dict_product_total})
                    user_team_dict.update({user_id.name: dict_prodct})

        if not user_team_dict:
            raise ValidationError("Record's Not Exist...")

        dict_final_total['Name'] = 'Final Total :'
        dict_final_total['Quantity'] = final_qty
        return {
            'doc_ids': user_team_dict,
            'doc_model': report.model,
            'final_total': dict_final_total,
            'header_list': header_list,
            'currency_list': currency_list,
            'data': data,
        }
