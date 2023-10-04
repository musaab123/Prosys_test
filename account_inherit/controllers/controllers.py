# -*- coding: utf-8 -*-
# from odoo import http


# class AccountInherit(http.Controller):
#     @http.route('/account_inherit/account_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_inherit/account_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_inherit.listing', {
#             'root': '/account_inherit/account_inherit',
#             'objects': http.request.env['account_inherit.account_inherit'].search([]),
#         })

#     @http.route('/account_inherit/account_inherit/objects/<model("account_inherit.account_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_inherit.object', {
#             'object': obj
#         })
