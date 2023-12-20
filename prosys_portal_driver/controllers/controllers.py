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
    

    def _prepare_picking_default_values(self,picking_id):
        vals = {
            'move_ids': [],
            'picking_type_id': picking_id.picking_type_id.return_picking_type_id.id or picking_id.picking_type_id.id,
            'state': 'draft',
            'origin': _("Return of %s") % picking_id.name,
            
        }
        # TestPickShip.test_mto_moves_return, TestPickShip.test_mto_moves_return_extra,
        # TestPickShip.test_pick_pack_ship_return, TestPickShip.test_pick_ship_return, TestPickShip.test_return_lot
        if picking_id.location_dest_id:
            vals['location_id'] = picking_id.location_dest_id.id
        if picking_id.location_id:
            vals['location_dest_id'] = picking_id.location_id.id
        return vals
    
    @http.route(['/portal/return_order'], type='json', auth="public", website=True)
    def return_order(self, **kw):
        vals = kw.get('vals')
        new_picking_created = False
        for line in vals:
            order = request.env['sale.order'].sudo().browse(line.get('order_id'))
            sale_order_line = request.env['sale.order.line'].sudo().browse(line.get('line_id'))

            if not sale_order_line:
                continue
            if int(line.get('quantity')) <= 0 or  int(line.get('quantity')) > sale_order_line.product_uom_qty:
                continue
           
            for picking_id in order.picking_ids:
                for move_line in picking_id.move_line_ids:

                    if move_line.product_id.id == sale_order_line.product_id.id:
                        if picking_id.state == 'done':

                            # move_line.quantity_done = sale_order_line.product_uom_qty - int(line.get('quantity'))
                            # print("new quantity state !=done")
                            # print("quantity",move_line.quantity_done)


                            # picking_id.action_confirm()
                            # picking_id.action_assign()
                        # else:
                            if new_picking_created == False:
                                new_picking = picking_id.copy(self._prepare_picking_default_values(picking_id))
                                new_picking_created = True
                        
                            print("new picking",new_picking)
                            

                            request.env['stock.move'].sudo().create({
                                "product_id" :move_line.product_id.id,
                                "product_uom_qty": int(line.get('quantity')),
                                # "uom_id":sale_order_line.product_id.uom_id.id,
                                "picking_id":new_picking.id,
                                "location_id":picking_id.location_dest_id.id,
                                "location_dest_id": picking_id.location_id.id,
                                "name": _("Return of %s") % picking_id.name,
                                "quantity_done":int(line.get('quantity'))

                            })
                            # request.session['success_message'] = _("Customer added successfully")
                            # for return_order_line in new_picking.move_line_ids:
                            #     return_order_line.quantity_done = return_order_line.product_uom_qty
                            print("before confirm",line)

                            new_picking.note = kw.get("reason"," ")
                        
                            new_picking.sale_id = order.id
                            for sale_order_line_rec in order.order_line:
                                if sale_order_line_rec.product_id.id == move_line.product_id.id:
                                    sale_order_line_rec.qty_delivered =  sale_order_line_rec.qty_delivered - int(line.get('quantity'))

                            print("Done")
        # if new_picking_created:
            # new_picking.action_confirm()
            # new_picking.action_assign()
            # new_picking.state ='done'

        
    
    @http.route(['/portal/create_invoice'], type='json', auth="public", website=True)
    def create_invoice(self, **kw):
        vals = kw.get('vals')

        order = request.env['sale.order'].sudo().browse(vals[0].get('order_id'))
        print("order ---------------------->", order)
        invoice =order._create_invoices()
        invoice.action_post()
        print("invoice   ------->", invoice)

        return {'success': True, 'invoice_id': invoice.id}
                
            

    @http.route('/my/request-thank-you', website=True, page=True,auth='public', csrf=False)
    def maintenance_request_thanks(self):
        """Controller to redirect to the success page when return order
         submitted successfully"""
        return request.render("prosys_portal_driver.customers_request_thank_page")
    
    
        
