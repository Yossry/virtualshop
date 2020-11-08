# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductSalesWizard(models.TransientModel):
    _name = 'product.sale.wizard'
    _description = "Product Sales Wizard"

    from_date = fields.Date(required=True, default=fields.Date.today)
    to_date = fields.Date(required=True, default=fields.Date.today)
    report_type = fields.Selection([
        ('day_wise', 'Day Wise (Weekly)'), ('summary', 'Summary')],
        default='summary')
    report_of = fields.Selection([
        ('product', 'Product'), ('category', 'Product Category')],
        default='category')
    report_by = fields.Selection([
        ('sales_team', 'Sales Team'), ('sales_person', 'Sales Person')],
        default='sales_team')
    user_id = fields.Many2many('res.users', default=lambda self: self.env.user)
    team_id = fields.Many2many('crm.team')

    def print_report(self):
        sale_domain = [('date_order', '>=', self.from_date),
                       ('date_order', '<=', self.to_date),
                       ('state', '=', 'sale')]
        module = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'point_of_sale'), ('state', '=', 'installed')], limit=1)
        pos_domain = []
        if module and self.env.user.has_group('point_of_sale.group_pos_user') and self.env.user.has_group('stock.group_stock_user'):
            if self.env['pos.order'].search([]):
                pos_domain = [('date_order', '>=', self.from_date),
                              ('date_order', '<=', self.to_date)]

        data = {
            'user_id': self.user_id.ids,
            'team_id': self.team_id.ids,
            'report_type': self.report_type,
            'report_of': self.report_of,
            'report_by': self.report_by,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'sale_domain': sale_domain,
            'pos_domain': pos_domain,
        }
        if self.report_type == 'summary':
            return self.env.ref('product_sales_report.report_product_sales_summary_ip').report_action(self, data=data)
        if self.report_type == 'day_wise':
            return self.env.ref('product_sales_report.report_product_sales_weekly_ip').report_action(self, data=data)
