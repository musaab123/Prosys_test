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
        if request.env.user._is_admin():
            domain = []
        else:
            domain = [('employee_id', '=', request.env.user.employee_id.id)]
        if 'loan_count' in counters:
            loan_count = request.env['employee.loan'].sudo().search_count(domain) \
                if request.env['employee.loan'].sudo().check_access_rights('read', raise_exception=False) else 0
            values['loan_count'] = loan_count
        return values

    def _get_searchbar_loans_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'employee': {'input': 'employee', 'label': _('Search in Employee')},
            'payment_method': {'input': 'payment_method', 'label': _('Search with payment method')},
            'department_id': {'input': 'department_id', 'label': _('Search with department_id')},
            'loan_type_id': {'input': 'v', 'label': _('Search with loan_type_id')},
   }

    def _get_search_loans_domain(self, search_in, search):
        search_domain = []
        if search_in in ('name', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('employee', 'all'):
            search_domain = OR([search_domain, [('employee_id', 'ilike', search)]])
        if search_in in ('payment_method', 'all'):
            search_domain = OR([search_domain, [('payment_method', 'ilike', search)]])
        return search_domain

 

    def _get_searchbar_loans_sortings(self):
        return {
    
            'payment_method': {'label': _('Payment Mode'), 'order': 'payment_method', 'sequence': 3},
            'department_id': {'label': _('Category'), 'order': 'department_id', 'sequence': 4},
            'loan_type_id': {'label': _('Category'), 'order': 'loan_type_id', 'sequence': 4},
            'date': {'label': _('Date'), 'order': 'date', 'sequence': 4},

        }

    def _get_searchbar_loans_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'date': {'label': _('Date'), 'order': 'date', 'sequence': 4},
            
        }
        # return dict(sorted(values.items(), key=lambda item: item[1]["order"]))




    def _get_groupby_loans_mapping(self):
        return {
            'payment_method': 'payment_method',
            'date': 'date',
        }


    def _get_order(self, order, groupby):
        groupby_mapping = self._get_groupby_loans_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)
# stop hear ---------------------------------------------------------------------------------------------------------

    @http.route(['/my/loan', '/my/loan/page/<int:page>'], type='http', auth="user", website=True)
    def portal_loans(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        loans = request.env['employee.loan'].sudo()
        _items_per_page = 20

        if request.env.user._is_admin():
            domain = []
        else:
            domain = [('employee_id', '=', request.env.user.employee_id.id)]
        searchbar_sortings = self._get_searchbar_loans_sortings()
        searchbar_groupby = self._get_searchbar_loans_groupby()
        searchbar_inputs = self._get_searchbar_loans_inputs()
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': domain},
            # 'approved': {'label': _('Approved Time Off'), 'domain': [('state', '=', 'validate')]},
            # 'to_approve': {'label': _('To Approve'), 'domain': [('state', '=', 'confirm')]},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        if not groupby:
            groupby = 'none'

        if search and search_in:
            domain += self._get_search_loans_domain(search_in, search)

        loans_count = loans.search_count(domain)

        pager = portal_pager(
            url="/my/loan",
            url_args={'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby, 'sortby': sortby},
            total=loans_count,
            page=page,
            step=_items_per_page
        )

        order = self._get_order(order, groupby)
        loans = loans.search(domain, order=order, limit=_items_per_page, offset=pager['offset'])
        request.session['my_loan_history'] = loans.ids[:100]

        groupby_mapping = self._get_groupby_loans_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_loans = [loan.concat(*g) for k, g in groupbyelem(loans, itemgetter(group))]
        else:
            grouped_loans = [loans]
        allocations = loans.search([('employee_id', '=', request.env.user.employee_id.id)])
      
        values.update({
            'grouped_loans': grouped_loans,
            'page_name': 'loan',
            'pager': pager,
            'default_url': '/my/loan',
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
        return request.render("portal_loan.portal_my_loan_list", values)



    @http.route(['/create/loan'], type='http', auth="user", website=True)
    def loan_create(self, **post):
        employee = request.env.user.employee_id
        domain=[]
        department_id = request.env['hr.department'].sudo().search(domain)
        loan_type_id = request.env['employee.loan.type'].sudo().search(domain)
        manager_id = request.env['hr.employee'].sudo().search(domain)

        payment_meths = ['by_payslip']
        values = {
            'employee': employee,
            'department_id': department_id,
            'manager_id': manager_id,
            'payment_meths': payment_meths,
            'loan_type_id': loan_type_id,
        }
        return request.render("portal_loan.portal_apply_loan", values)


    
    @http.route(['/save/loan'], type='http', auth="user", website=True)
    def save_loan(self, **post):
        field_list = ['date', 'product_id', 'total_amount', 'payment_mode' ,'name','company']
        value = []
        department_id_domain=[]
        department_id = request.env['hr.department'].sudo().search(department_id_domain)
        loan_type_id = request.env['employee.loan.type'].sudo().search(department_id_domain)
        manager_id = request.env['hr.employee'].sudo().search(department_id_domain)

        employee = request.env.user.employee_id
        payment_method = request.env['employee.loan'].payment_method
        payment_meths = ['by_payslip']
        # company = request.env['res.company'].search(domain)
        # company = request.env['res.company'].search([('company_id', '=', False), ('company_id', '=', request.env.user.company_id.id)])

        for key in post:
            value.append(post[key])
            print("keeeeey",key, "vaaaaaalue", value)
  


       
        vals = {
            'employee_id': request.env.user.employee_id.id,
            'loan_type_id': post.get('loan_type_id'),
            'department_id': post.get('department_id'),
            'manager_id': post.get('manager_id'),
            'term': post.get('term'),


            'date': post.get('date'),
            'payment_method': post.get('payment_method'),
            # 'company': company,
            'loan_amount': post.get('loan_amount'),
            'name': post.get('name'),
            'notes': post.get('notes'),

        }
        print("ooooooooooooooo",vals)
        request.env['employee.loan'].sudo().create(vals)
        return request.redirect('/my/loan')