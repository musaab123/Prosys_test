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
from odoo.exceptions import RedirectWarning, UserError, ValidationError

DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')


class PortalProductSales(CustomerPortal):
    

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'salesmen_count' in counters:

            sales = request.env['sale.order'].sudo().search([('user_id','=',request.env.user.id)])
            values['salesmen_count'] = len(sales)
        return values

    def _get_searchbar_salesmen_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'user': {'input': 'user', 'label': _('Search in User')},
            'date_order': {'input': 'date_order', 'label': _('Search with Quotation Date')},
        }

    def _get_search_salesmen_domain(self, search_in, search):
        search_domain = []
        if search_in in ('name', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('user', 'all'):
            search_domain = OR([search_domain, [('user_id', 'ilike', search)]])
        if search_in in ('date_order', 'all'):
            search_domain = OR([search_domain, [('date_order', 'ilike', search)]])
        return search_domain

    def _get_searchbar_salesmen_sortings(self):
        return {
            'name': {'label': _('Name'), 'order': 'name asc', 'sequence': 1},
        }

    def _get_searchbar_salesmen_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'name': {'input': 'name', 'label': _('Name'), 'order': 2},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _get_groupby_salesmen_mapping(self):
        return {
            'name': 'name',
        }

    def _get_order(self, order, groupby):
        groupby_mapping = self._get_groupby_salesmen_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)

    @http.route(['/my/salesrequest', '/my/salesrequest/page/<int:page>'], type='http', auth="user", website=True)
    def portal_salesmen(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        sales = request.env['sale.order'].sudo()
        _items_per_page = 20

        # if request.env.user._is_admin():
        #     domain = []
        # else:
        domain = [('user_id', '=', request.env.user.id)]
        searchbar_sortings = self._get_searchbar_salesmen_sortings()
        searchbar_groupby = self._get_searchbar_salesmen_groupby()
        searchbar_inputs = self._get_searchbar_salesmen_inputs()
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': domain},
        }

        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        if not groupby:
            groupby = 'none'

        if search and search_in:
            domain += self._get_search_salesmen_domain(search_in, search)

        salesmen_count = sales.search_count(domain)

        pager = portal_pager(
            url="/my/salesrequest",
            url_args={'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby, 'sortby': sortby},
            total=salesmen_count,
            page=page,
            step=_items_per_page
        )

        order = self._get_order(order, groupby)
        saless = sales.search(domain, order=order, limit=_items_per_page, offset=pager['offset'])
        # request.session['my_leave_history'] = saless.ids[:100]

        groupby_mapping = self._get_groupby_salesmen_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_salesmen = [sales.concat(*g) for k, g in groupbyelem(saless, itemgetter(group))]
        else:
            grouped_salesmen = [saless]
        # raise UserError(grouped_salesmen)
        values.update({
            'grouped_salesmen': grouped_salesmen,
            'page_name': 'sales_request',
            'pager': pager,
            'default_url': '/my/salesrequest',
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
        return request.render("prosys_product_portal.portal_my_salesmen_list", values)
    
    







    @http.route(['/add/products/salesmen', '/add/products/salesmen/page/<int:page>'], type='http', auth="public", website=True)
    def portal_add_salesmen_products(self, **kw):
        sertificate_obj = request.env['product.template'].sudo()
        domain = []
        product = sertificate_obj.search(domain)
        vals = {'product':product ,'page_name':'product_list_view'}
  
        return request.render("prosys_product_portal.portal_add_product_salesmen_list" ,vals)


    @http.route(['/check/submit_sale_add_product'], type='json', auth="user", website=True)
    def get_submit_sales_add_product(self,  **kw):
        location =  kw['location'] if  kw['location'] else False
        phone =  kw['phone'] if  kw['phone'] else False
        company =  kw['company'] if  kw['company'] else False
        # currency =  kw['currency'] if  kw['currency'] else False
        products_list =  kw['products_list'] if  kw['products_list'] else False

        if location:
            partner = request.env['res.partner'].sudo().search([('phone','=',phone),('company_id','=',int(company)),('street','=',location)])
        else:
            partner = request.env['res.partner'].sudo().search([('phone','=',phone),('company_id','=',int(company))])

        user_id = False
        if request.env.user:
            user_id = request.env.user.id
        if len(partner) == 1:

            order_line = []
            if products_list:
                for pro in products_list:
                    product = request.env['product.product'].sudo().browse(int(pro['product_id']))
                    vals = {
                        'name':product.name,
                        'product_id':product.id,
                        'discount_method':'per',
                        'discount_amount':pro['discount'],
                        'product_uom_qty':pro['product_uom_qty'],
                    }
                    order_line.append((0,0,vals))

            sales = request.env['sale.order'].sudo().create({
                'partner_id':partner.id,
                'company_id':int(company),
                'user_id':user_id,
                'discount_type':'line',
                'order_line':order_line,
            })

            return {
                    'alert':'done',
                    'url':'/add/products/confirmed_soorder/%s'%sales.id
                }
        elif len(partner) > 1:
            branchs = []
            for part in partner:
                if part.street:
                    branchs.append(part.street)
            return {
                    'alert':'show branch',
                    'branchs':branchs,
                }


        else:
            partner_val = {
                'name':phone,
                'email':phone,
                'phone':phone,
                'company_id':company,
                'property_stock_customer':False,
                'property_stock_supplier':False,
                'property_payment_term_id':False,
                'property_account_position_id':False,
            }
            partner = request.env['res.partner'].sudo().create(partner_val)

            order_line = []
            if products_list:
                for pro in products_list:
                    product = request.env['product.product'].sudo().browse(int(pro['product_id']))
                    vals = {
                        'name':product.name,
                        'product_id':product.id,
                        'discount_method':'per',
                        'discount_amount':pro['discount'],
                        'product_uom_qty':pro['product_uom_qty'],
                    }
                    order_line.append((0,0,vals))

            sales = request.env['sale.order'].sudo().create({
                'partner_id':partner.id,
                'company_id':int(company),
                'user_id':user_id,
                'discount_type':'line',
                'order_line':order_line,
            })

            return {
                    'alert':'done',
                    'url':'/add/products/confirmed_soorder/%s'%sales.id
                }

    @http.route(['/add/products/confirmed_soorder/<int:sale_id>'], type='http', auth="user", website=True, sitemap=False)
    def confirm_salesmen_order(self,sale_id=None):
        sale_order = request.env['sale.order'].sudo().browse(int(sale_id))
        

        return request.render("prosys_product_portal.portal_add_product_salesmen_confirmed", {'sale_order': sale_order})

   
   



   