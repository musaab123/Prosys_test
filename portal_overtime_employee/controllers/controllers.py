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

# DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')


class PortalOvertime(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if request.env.user._is_admin():
            domain = []
        else:
            domain = [('employee_id', '=', request.env.user.employee_id.id)]
        if 'overtime_count' in counters:
            overtime_count = request.env['overtime.request'].sudo().search_count(domain) \
                if request.env['overtime.request'].sudo().check_access_rights('read', raise_exception=False) else 0
            values['overtime_count'] = overtime_count
        return values

    def _get_searchbar_over_time_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'employee': {'input': 'employee', 'label': _('Search in Employee')},
            'start_date': {'input': 'start_date', 'label': _('Search with payment date')},
            'department_id': {'input': 'department_id', 'label': _('Search with department_id')},
   }

    def _get_search_over_time_domain(self, search_in, search):
        search_domain = []
        if search_in in ('department_id', 'all'):
            search_domain = OR([search_domain, [('department_id', 'ilike', search)]])
        if search_in in ('employee', 'all'):
            search_domain = OR([search_domain, [('employee_id', 'ilike', search)]])
        if search_in in ('start_date', 'all'):
            search_domain = OR([search_domain, [('start_date', 'ilike', search)]])
        return search_domain

 

    def _get_searchbar_over_time_sortings(self):
        return {
    
            'start_date': {'label': _('Start Date'), 'order': 'start_date', 'sequence': 3},
           

        }

    def _get_searchbar_over_time_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'start_date': {'label': _('Start Date'), 'order': 'start_date', 'sequence': 4},
            
        }




    def _get_groupby_over_time_mapping(self):
        return {
            'start_date': 'start_date',
        }


    def _get_order(self, order, groupby):
        groupby_mapping = self._get_groupby_over_time_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)

    @http.route(['/my/overtime', '/my/overtime/page/<int:page>'], type='http', auth="user", website=True)
    def portal_over_time(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        overs = request.env['overtime.request'].sudo()
        _items_per_page = 20

        if request.env.user._is_admin():
            domain = []
        else:
            domain = [('employee_id', '=', request.env.user.employee_id.id)]
        searchbar_sortings = self._get_searchbar_over_time_sortings()
        searchbar_groupby = self._get_searchbar_over_time_groupby()
        searchbar_inputs = self._get_searchbar_over_time_inputs()
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': domain},
           
        }

        if not sortby:
            sortby = 'start_date'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        if not groupby:
            groupby = 'none'

        if search and search_in:
            domain += self._get_search_over_time_domain(search_in, search)

        overtime_count = overs.search_count(domain)

        pager = portal_pager(
            url="/my/overtime",
            url_args={'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby, 'sortby': sortby},
            total=overtime_count,
            page=page,
            step=_items_per_page
        )

        order = self._get_order(order, groupby)
        overs = overs.search(domain, order=order, limit=_items_per_page, offset=pager['offset'])
        request.session['my_overtime_history'] = overs.ids[:100]

        groupby_mapping = self._get_groupby_over_time_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_overtime = [overtime.concat(*g) for k, g in groupbyelem(overs, itemgetter(group))]
        else:
            grouped_overtime = [overs]
        allocations = overs.search([('employee_id', '=', request.env.user.employee_id.id)])
      
        values.update({
            'grouped_overtime': grouped_overtime,
            'page_name': 'overtime',
            'pager': pager,
            'default_url': '/my/overtime',
            'search_in': search_in,
            'search': search,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("portal_overtime_employee.portal_my_over_time", values)



    @http.route(['/create/overtime'], type='http', auth="user", website=True)
    def overtime_create(self, **post):
        employee = request.env.user.employee_id
        domain=[]
        department_id = request.env['hr.department'].sudo().search(domain)
        department_manager_id = request.env['hr.employee'].sudo().search(domain)

        values = {
            'employee': employee,
            'department_id': department_id,
            'department_manager_id': department_manager_id,

           
        }
        return request.render("portal_overtime_employee.portal_apply_employee_overtime", values)
    




    @http.route(['/save/overtime'], type='http', auth="user", website=True)
    def save_overtime(self, **post):
        field_list = ['date', 'product_id', 'total_amount', 'start_date','end_date' ,'name','company']
        value = []
        department_id_domain=[]
        department_id = request.env['hr.department'].sudo().search(department_id_domain)
        department_manager_id = request.env['hr.employee'].sudo().search(department_id_domain)

        employee = request.env.user.employee_id
    
        # company = request.env['res.company'].search(domain)
        # company = request.env['res.company'].search([('company_id', '=', False), ('company_id', '=', request.env.user.company_id.id)])

        for key in post:
            value.append(post[key])
            print("keeeeey",key, "vaaaaaalue", value)
       
        vals = {
            'employee_id': request.env.user.employee_id.id,
            'department_id': post.get('department_id'),
            'department_manager_id': post.get('department_manager_id'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),

           
            'notes': post.get('notes'),

        }
        print("ooooooooooooooo",vals)
        request.env['overtime.request'].sudo().create(vals)
        return request.redirect('/my/overtime')


    
