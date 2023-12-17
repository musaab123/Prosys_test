# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import http, _
from operator import itemgetter
from pytz import timezone, UTC
from odoo.addons.resource.models.resource import float_to_time
from collections import OrderedDict
from collections import namedtuple
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime
from odoo.tools import groupby as groupbyelem



class PortalAttendanceKnk(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        counters.append('driver_quotation_count')
        values = super()._prepare_home_portal_values(counters)
        domain = [('name', '=', request.env.user.name)]
        
        if 'driver_quotation_count' in counters:
            employee_id = request.env.user.employee_id.id
            domain = [('driver_id','=',employee_id),('state','in',('draft', 'sent'))]
            driver_quotation_count = request.env['sale.order'].sudo().search_count(domain)
            if driver_quotation_count:
                values['driver_quotation_count'] = driver_quotation_count
                print("counter -------->",driver_quotation_count)
            else:
                values['driver_quotation_count'] = 0
                print("counte of else state")



        if 'driver_sale_order_count' in counters:
            employee_id = request.env.user.employee_id.id
            domain = [('driver_id','=',employee_id),('state','in',('sale','done'))]
            driver_sale_order_count = request.env['sale.order'].sudo().search_count(domain)
            values['driver_sale_order_count'] = driver_sale_order_count

        

        if 'driver_invoice_count' in counters:
            employee_id = request.env.user.employee_id.id
            domain = [('driver_id','=',employee_id),('state','in',('draft','posted'))]

            driver_invoice_count = request.env['account.move'].sudo().search_count(domain)
                
            values['driver_invoice_count'] = driver_invoice_count
        return values
    

    @http.route(['/my/driver/saleorder', '/my/driver/saleorder/page/<int:page>'], type='http', auth="user", website=True)
    def portal_driver_saleorder(self, page=1, **kw):
        _items_per_page = 20

        employee_id = request.env.user.employee_id.id
        domain = [('driver_id','=',employee_id),('state','in',('sale','done'))]

        driver_sale_order_count = request.env['sale.order'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/driver/saleorder",
            url_args={},
            total=driver_sale_order_count,
            page=page,
            step=_items_per_page
        )

        orders = request.env['sale.order'].sudo().search(domain)
      
        values={
            'page_name': 'driver orders',
            'pager': pager,
            'default_url': '/my/driver/saleorder',
            'orders':orders
        }
        return request.render("prosys_portal_driver.portal_my_order_driver_list", values)
    


    @http.route(['/my/driver/quotations', '/my/driver/quotations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_driver_quotation(self, page=1, **kw):
        _items_per_page = 20

        employee_id = request.env.user.employee_id.id
        domain = [('driver_id','=',employee_id),('state','in',('draft', 'sent'))]

        driver_quotation_count = request.env['sale.order'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/driver/quotations",
            url_args={},
            total=driver_quotation_count,
            page=page,
            step=_items_per_page
        )

        quotations = request.env['sale.order'].sudo().search(domain)
        values={
            'page_name': 'driver quotation',
            'pager': pager,
            'default_url': '/my/driver/quotations',
            'quotations':quotations
        }
        return request.render("prosys_portal_driver.portal_my_quotations_driver_list", values)


    @http.route(['/my/driver/invoice', '/my/driver/invoice/page/<int:page>'], type='http', auth="user", website=True)
    def portal_driver_invoice(self, page=1, **kw):
        _items_per_page = 20

        employee_id = request.env.user.employee_id.id
        domain = [('driver_id','=',employee_id),('state','in',('draft','posted'))]

        driver_invoice_count = request.env['account.move'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/driver/invoice",
            url_args={},
            total=driver_invoice_count,
            page=page,
            step=_items_per_page
        )

        invoices = request.env['account.move'].sudo().search(domain)
      
        values={
            'page_name': 'driver invoice',
            'pager': pager,
            'default_url': '/my/driver/invoice',
            'invoices':invoices
        }
        return request.render("prosys_portal_driver.portal_my_invoice_driver_list", values)
    


   