# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Vishnu P(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
""" add field requisition_order in purchase order"""
from odoo import models, fields

class PurchaseOrder(models.Model):
    """ inherit purchase.order model """

    _inherit = 'purchase.order.line'

    flag=fields.Boolean("")


class PurchaseOrder(models.Model):
    """ inherit purchase.order model """

    _inherit = 'purchase.order'

    requisition_order = fields.Char(string='Requisition Order',
                                    help='Requisition Order')

    purchase_plan_ids=fields.Many2many("purchase.plan",string="Purchase Plan")



    def button_confirm(self):
        for order in self:
            product_qtty=0.0
            category_qty=0.0
            flag=False
            purchase_plan_id=self.env['purchase.plan.actual'].search([('purchase_plan_id','in',order.purchase_plan_ids.ids)])
            for line in order.order_line:
                for rec_plan in purchase_plan_id:

                    if rec_plan.product_category_type=='product' and rec_plan.product_id:
                        if line.product_id==rec_plan.product_id:
                            product_qtty=rec_plan.product_qty
                            line.flag=True

                            product_qtty=product_qtty+line.product_qty


                            rec_plan.product_qty=product_qtty





                    if rec_plan.product_category_type=='category' and  rec_plan.category_id:
                        if line.product_id.categ_id==rec_plan.category_id :
                            if line.flag==False:
                                category_qty=rec_plan.product_qty
                                print ("############################3",category_qty)
                                category_qty=category_qty+line.product_qty
                    
                                rec_plan.product_qty=category_qty







            #     order.action_create_invoice()
            # if order.ore_purchased:
            #     for record in order.order_line:
            #         for recordd in order.picking_ids.move_ids_without_package:
            #             recordd.batch_no=record.batch_No


        super(PurchaseOrder, self).button_confirm()

