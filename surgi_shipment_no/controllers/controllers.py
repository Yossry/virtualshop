# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiShipmentNo(http.Controller):
#     @http.route('/surgi_shipment_no/surgi_shipment_no/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_shipment_no/surgi_shipment_no/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_shipment_no.listing', {
#             'root': '/surgi_shipment_no/surgi_shipment_no',
#             'objects': http.request.env['surgi_shipment_no.surgi_shipment_no'].search([]),
#         })

#     @http.route('/surgi_shipment_no/surgi_shipment_no/objects/<model("surgi_shipment_no.surgi_shipment_no"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_shipment_no.object', {
#             'object': obj
#         })
