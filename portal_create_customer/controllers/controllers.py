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


class PortalAttendanceKnk(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = [('name', '=', request.env.user.name)]
        if 'customers_count' in counters:
            customers_count = request.env['res.partner'].sudo().search_count(domain) 
                
            values['customers_count'] = customers_count
        return values
    


    @http.route(['/my/customer', '/my/customer/page/<int:page>'], type='http', auth="user", website=True)
    def portal_customer(self, **kw):
        # values = self._prepare_portal_layout_values()
        customers_obj = request.env['res.partner'].sudo()
        domain = [('name', '=', request.env.user.name)]
        customer_create = customers_obj.search(domain)
        vals = {'customer_create':customer_create ,'page_name':'customer_list_view'}
        return request.render("portal_create_customer.portal_my_customer_list", vals)


    @http.route(['/my/customers/<model("res.partner"):partner_id>'], type='http', auth="user", website=True)
    def portal_certificate_form(self, partner_id , **kw):
        vals = {"partner":partner_id}
        return request.render("portal_create_customer.payslip_portal_template", vals)
    

    
    @http.route(['/create/customer'], type='http', auth="user", website=True)
    def customer_create(self, **post):
        domain=[]
        jop_id = request.env['jop.postion'].sudo().search(domain)
        region_id = request.env['regional.area'].sudo().search(domain)
        district_id = request.env['district.district'].sudo().search(domain)
        # categ_id = request.env['clint.activty'].sudo().search(domain)
        country_id = request.env['res.country'].sudo().search(domain)
        state_id = request.env['res.country.state'].sudo().search(domain)
        


        
        company_types = ['person','company']
    
        values = {
            'jop_id': jop_id,
            'region_id': region_id,
            'district_id': district_id,
            'country_id': country_id,
            'state_id': state_id,
            # 'categ_id': categ_id,
            'company_types': company_types,

        }
        return request.render("portal_create_customer.portal_apply_create_customer", values)
    

    @http.route(['/save/customer'], type='http', auth="user", website=True)
    def save_expense(self, **post):
        field_list = ['date', 'product_id', 'total_amount', 'payment_mode' ,'name','company']
        value = []
        company_type = request.env['res.partner'].company_type
        company_types = ['person','company']
        selected_categ_ids = [int(cat_id.split('_')[-1]) for cat_id in post if cat_id.startswith('categ_id_') and post[cat_id] == 'on']

        for key in post:
            value.append(post[key])
            print("keeeeey",key, "vaaaaaalue", value)
       
        vals = {
            'jop_id': post.get('jop_id'),
            'region_id': post.get('region_id'),
            'company_type': post.get('company_type'),
            'district_id': post.get('district_id'),
            'name': post.get('name'),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'zip': post.get('zip'),
            'city': post.get('city'),
            'state_id': post.get('state_id'),
            'country_id': post.get('country_id'),
            'mobile': post.get('mobile'),
            'additional_code': post.get('additional_code'),
            'buliding_number': post.get('buliding_number'),
            'vat': post.get('vat'),
            'cr': post.get('cr'),
            'partner_latitude': post.get('partner_latitude'),
            'partner_longitude': post.get('partner_longitude'),

            'trade_name': post.get('trade_name'),

            # 'categ_id': [(6, 0, selected_categ_ids)],

        }
        print("ooooooooooooooo",vals)
        request.env['res.partner'].sudo().create(vals)
        request.session['success_message'] = _("Customer added successfully")
        return request.redirect('/my/customer')


   