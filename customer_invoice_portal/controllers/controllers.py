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
from odoo.tools import date_utils, groupby as groupbyelem


DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')


class PortalColloctor(CustomerPortal):
  

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

       
        if 'customer_inv_count' in counters:
            values["customer_inv_count"] = request.env['account.move'].sudo().search_count([
                ('move_type', '=', 'out_invoice'),
                ('payment_state', 'in', ['not_paid', 'partial']),
                ('collecter_id', '=', request.uid)])
          
        return values
    






    @http.route(['/my/customer/invoices', '/my/customer/invoices/page/<int:page>'], type='http', auth="user", website=True)
    def _due_customers_portal_view_list(self, page=1, sortby='invoice_date', filterby='all', search="", search_in="", **kw):
        values = self._prepare_portal_layout_values()
        customer_inv_obj = request.env['account.move']
        domain = [
                ('move_type', '=', 'out_invoice'), 
                ('payment_state', 'in', ['not_paid', 'partial']), # Filter by invoices
                ('collecter_id', '=', request.uid)
            ]
        search_list = {
            'All': {'label': _('All'), 'input':'All', 'domain': []},
            'Name': {'label': _('Invoice Name'), 'input':'Name', 'domain': [('name', 'ilike', search)]},
            'Partner': {'label': _('Partner'), 'input':'Partner', 'domain': [('partner_id.name', 'ilike', search)]},
            'Invoice Date': {'label': _('Invoice Date'), 'input':'Invoice Date', 'domain': [('invoice_date', 'ilike', search)]},
            'Invoice Due Date': {'label': _('Invoice Due Date'), 'input':'Invoice Due Date', 'domain': [('invoice_date_due', 'ilike', search)]},
        }

       
        if search_in in search_list:
            domain += search_list[search_in]['domain']
        else:
            pass

        if kw == {}:
            pass
        elif kw['begin_date'] and kw['end_date'] and kw['partner_id']:
            domain += [('invoice_date_due', '>=', kw['begin_date']), ('invoice_date_due', '<=', kw['end_date']), ('partner_id', '=', int(kw['partner_id']))]

        searchbar_sortings = {
            'invoice_date': {'label': _('Newest Invoice'), 'order': 'invoice_date desc, invoice_date desc'},
            'invoice_date_due': {'label': _('Newest Due Invoice'), 'order': 'invoice_date_due desc, invoice_date_due desc'},
            'name': {'label': _('Name/Ref#'), 'order': 'name asc, name asc'},
            'amount_total_signed': {'label': _('Total'), 'order': 'amount_total_signed desc, amount_total_signed desc'},
        }

        order = searchbar_sortings[sortby]['order']

        total_invoices = customer_inv_obj.sudo().search_count(domain)

        items_per_page = 15

        pager = portal_pager(
            url='/my/customer/invoices',
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
            total=total_invoices,
            page=page,
            step=items_per_page
        )

        customer_inv = customer_inv_obj.sudo().search(
            domain,
            order=order,
            limit=items_per_page,
            offset=pager['offset']
        )

        values.update ({
            'customer_inv_count': total_invoices,
            'customer_inv': customer_inv,
            'page_name': 'my_customer_inv',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'filterby': filterby,
            'searchbar_inputs': search_list,
            'search_in': search_in,
            'search': search,
            'res_partner': request.env['res.partner'].sudo().search([('id', 'in', customer_inv.partner_id.ids)]),
            'default_url': '/my/customer/invoices',
        })
        return http.request.render('customer_invoice_portal.customer_invoice_list_view_portal', values)

        
       




    