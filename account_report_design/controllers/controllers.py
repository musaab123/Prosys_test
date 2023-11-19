# -*- coding: utf-8 -*-
# from odoo import http


# class AccountReportDesign(http.Controller):
#     @http.route('/account_report_design/account_report_design', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_report_design/account_report_design/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_report_design.listing', {
#             'root': '/account_report_design/account_report_design',
#             'objects': http.request.env['account_report_design.account_report_design'].search([]),
#         })

#     @http.route('/account_report_design/account_report_design/objects/<model("account_report_design.account_report_design"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_report_design.object', {
#             'object': obj
#         })
