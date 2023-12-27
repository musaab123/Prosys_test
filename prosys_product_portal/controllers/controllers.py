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


class PortalAttendanceKnk(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        
        domain = []
       
        product_count = request.env['product.template'].sudo().search_count(domain) 
              
        values['product_count'] = product_count
        return values
    

    @http.route(['/add/products','/add/products/<string:code>', '/add/products/page/<int:page>'], type='http', auth="public", website=True)
    def portal_add_products(self,code=None, **kw):
        if code:
            generator = request.env['qr.generator.model'].sudo().search([('unique_code','=',code)])
            if generator:
                sertificate_obj = request.env['product.template'].sudo()
                domain = []
                product = sertificate_obj.sudo().search(domain)
                vals = {'product':product ,'page_name':'product_list_view'}

        
                return request.render("prosys_product_portal.portal_add_product_list" ,vals)
            else:
                return request.render("prosys_product_portal.portal_add_product_not_allowed")
        else:
            return request.render("prosys_product_portal.portal_add_product_not_allowed")



    @http.route(['/check/get_product_by_barcode'], type='json', auth="none", website=True)
    def get_product_by_barcode(self,  **kw):
        if kw['barcode'] == 'False':
            barcode = False
        else:
            barcode =  kw['barcode'] if  kw['barcode'] else False
        product = request.env['product.product'].sudo().search_read([('barcode','=',barcode)], ['id', 'name','image_1920','lst_price'])
        if product:
            products = request.env['product.product'].browse(product[0]['id'])
            company = products.company_id.id
            # currency = products.company_id.currency_id.id

            return {
                    'product': product,
                    'company': company,
                    # 'currency': currency,
                    'alert':False,
                }
        else:
            return {
                    'product': False,
                    'company': False,
                    # 'currency': False,
                    'alert':'There is no product with this barcode',
                }


    
    @http.route(['/check/submit_add_product'], type='json', auth="none", website=True)
    def get_submit_add_product(self,  **kw):
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
        if len(partner) == 1:

            order_line = []
            if products_list:
                for pro in products_list:
                    product = request.env['product.product'].sudo().browse(int(pro['product_id']))
                    vals = {
                        'name':product.name,
                        'product_id':product.id,
                        'product_uom_qty':pro['product_uom_qty'],
                    }
                    order_line.append((0,0,vals))

            sales = request.env['sale.order'].sudo().create({
                'partner_id':partner.id,
                'company_id':int(company),
                'order_line':order_line,
            })

            return {
                    'alert':'done',
                    'url':'/add/products/confirmed_order/%s'%sales.id
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
                        'product_uom_qty':pro['product_uom_qty'],
                    }
                    order_line.append((0,0,vals))

            sales = request.env['sale.order'].sudo().create({
                'partner_id':partner.id,
                'company_id':int(company),
                'order_line':order_line,
            })

            return {
                    'alert':'done',
                    'url':'/add/products/confirmed_order/%s'%sales.id
                }

    @http.route(['/add/products/confirmed_order/<int:sale_id>'], type='http', auth="public", website=True, sitemap=False)
    def confirm_visitor_order(self,sale_id=None):
        sale_order = request.env['sale.order'].sudo().browse(int(sale_id))
        

        return request.render("prosys_product_portal.portal_add_product_list_confirmed", {'sale_order': sale_order})
   



   