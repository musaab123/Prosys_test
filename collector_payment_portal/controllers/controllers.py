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

DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')


class PortalColloctor(CustomerPortal):
  

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        
        domain = []
       
        payment_count = request.env['account.payment'].sudo().search_count(domain) 
              
        values['payment_count'] = payment_count
        return values

    def _get_searchbar_petty_cash_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'partner_id': {'input': 'partner_id', 'label': _('Search with Customer ')},
            'collecter_id': {'input': 'collecter_id', 'label': _('Search with Cash Collecters')},
   }

    def _get_search_petty_cash_domain(self, search_in, search):
        search_domain = []
        if search_in in ('name', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('partner_id', 'all'):
            search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
        if search_in in ('collecter_id', 'all'):
            search_domain = OR([search_domain, [('collecter_id', 'ilike', search)]])
        return search_domain

 

    def _get_searchbar_petty_cash_sortings(self):
        return {
    
            'collecter_id': {'label': _('Cash Collecters'), 'order': 'collecter_id', 'sequence': 3},
            'partner_id': {'label': _('Customer'), 'order': 'partner_id', 'sequence': 4},
            'date': {'label': _('Date'), 'order': 'date', 'sequence': 5},

        }

    def _get_searchbar_petty_cash_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'collecter_id': {'label': _('Cash Collecters'), 'order': 'collecter_id', 'sequence': 4},
            'partner_id': {'label': _('Customer'), 'order': 'partner_id', 'sequence': 4},
            'date': {'label': _('Date'), 'order': 'date', 'sequence': 5},


            
        }
        # return dict(sorted(values.items(), key=lambda item: item[1]["order"]))




    def _get_groupby_petty_cash_mapping(self):
        return {
            'collecter_id': 'collecter_id',
            # 'date': 'date',
        }


    def _get_order(self, order, groupby):
        groupby_mapping = self._get_groupby_petty_cash_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)
# stop hear ---------------------------------------------------------------------------------------------------------

    @http.route(['/my/payment', '/my/payment/page/<int:page>'], type='http', auth="user", website=True)
    def portal_petty_cash(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        payments = request.env['account.payment'].sudo()
        _items_per_page = 20
        domain = []
        # if request.env.user._is_admin():
        #     domain = []
        # else:
        #     domain = [('employee_id', '=', request.env.user.employee_id.id)]
        searchbar_sortings = self._get_searchbar_petty_cash_sortings()
        searchbar_groupby = self._get_searchbar_petty_cash_groupby()
        searchbar_inputs = self._get_searchbar_petty_cash_inputs()
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': domain},
            
        }

        if not sortby:
            sortby = 'collecter_id'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        if not groupby:
            groupby = 'none'

        if search and search_in:
            domain += self._get_search_petty_cash_domain(search_in, search)

        payment_count = payments.search_count(domain)

        pager = portal_pager(
            url="/my/payment",
            url_args={'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=_items_per_page
        )

        order = self._get_order(order, groupby)
        payments = payments.search(domain, order=order, limit=_items_per_page, offset=pager['offset'])
        request.session['my_expense_history'] = payments.ids[:100]

        groupby_mapping = self._get_groupby_petty_cash_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_payments = [payment.concat(*g) for k, g in groupbyelem(payments, itemgetter(group))]
        else:
            grouped_payments = [payments]
        # allocations = payments.search([('employee_id', '=', request.env.user.employee_id.id)])
      
        values.update({
            'grouped_payments': grouped_payments,
            'page_name': 'payment',
            'pager': pager,
            'default_url': '/my/payment',
            'search_in': search_in,
            'search': search,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            # 'allocations': leave_allocations,
        })
        return request.render("collector_payment_portal.portal_my_payment_colloctor", values)



    @http.route(['/create/payment'], type='http', auth="user", website=True)
    def payment_create(self, **kw):
        error_list =[]
        if not kw.get("date"):
            error_list.append("Name Field is requerd")
   
        domain=[]
        collecter_id = request.env['res.users'].sudo().search(domain)
        partner_id = request.env['res.partner'].sudo().search(domain)

        
        values = {
           
            'collecter_id': collecter_id,
            'partner_id': partner_id,
            'user': http.request.env.user

            # 'payment_modes': payment_modes,
           
        }
        return request.render("collector_payment_portal.portal_apply_colloctor_payment", values)


    
    @http.route(['/save/payment'], type='http', auth="user", website=True)
    def save_petty(self, **post):
        field_list = ['type_id', 'notes', 'amount', 'payment_date']
        value = []
        type_id_domain=[]
        collecter_id = request.env['res.users'].sudo().search(type_id_domain)
        partner_id = request.env['res.partner'].sudo().search(type_id_domain)

        for key in post:
            value.append(post[key])
            print("keeeeey",key, "vaaaaaalue", value)
       
       
        vals = {
            # 'employee_id': request.env.user.employee_id.id,
            'partner_id': post.get('partner_id'),
            'collecter_id': post.get('collecter_id'),
            'date': post.get('date'),
            'amount': post.get('amount'),
            'ref': post.get('ref'),

        }
        print("ooooooooooooooo",vals)
        request.env['account.payment'].sudo().create(vals)
        return request.redirect('/my/payment')