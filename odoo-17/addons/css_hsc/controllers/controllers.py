# -*- coding: utf-8 -*-
from odoo import http


# class CssHsc(http.Controller):
#     @http.route('/css_hsc/css_hsc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/css_hsc/css_hsc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('css_hsc.listing', {
#             'root': '/css_hsc/css_hsc',
#             'objects': http.request.env['css_hsc.css_hsc'].search([]),
#         })

#     @http.route('/css_hsc/css_hsc/objects/<model("css_hsc.css_hsc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('css_hsc.object', {
#             'object': obj
#         })
