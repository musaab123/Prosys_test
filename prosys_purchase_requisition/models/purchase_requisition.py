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
""" Purchase Requisition model"""
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class WorkLocation(models.Model):
    """ Inherit hr.department model"""

    _inherit = 'hr.work.location'

    location_id = fields.Many2one('stock.location',
                                             string='Destination Location',
                                             help='Department location')
    manager_id=fields.Many2one("hr.employee","Work Location Manager")



class PurchaseRequisition(models.Model):
    """ Model for storing purchase requisition """
    _name = 'employee.purchase.requisition'
    _description = 'Purchase Requisition'
    _inherit = "mail.thread", "mail.activity.mixin"

    name = fields.Char(string="Reference No", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True, help='Employee')
    dept_id = fields.Many2one('hr.department', string='Department',
                              related='employee_id.department_id', store=True,
                              help='Department')
    user_id = fields.Many2one('res.users', string='Requisition Responsible',
                              required=True,
                              help='Requisition responsible user')
    requisition_date = fields.Date(string="Requisition Date",
                                   default=lambda self: fields.Date.today(),
                                   help='Date of Requisition')
    receive_date = fields.Date(string="Received Date", readonly=True,
                               help='Receive Date')
    requisition_deadline = fields.Date(string="Requisition Deadline",
                                       help="End date of Purchase requisition")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 help='Company')
    requisition_order_ids = fields.One2many('requisition.order',
                                            'requisition_product_id',
                                            required=True)
    confirm_id = fields.Many2one('res.users', string='Confirmed By',
                                 default=lambda self: self.env.uid,
                                 readonly=True,
                                 help='User who Confirmed the requisition.')
    manager_id = fields.Many2one('res.users', string='Work Location Manager',
                                 readonly=True, help='Work Location Manager')
    requisition_head_id = fields.Many2one('res.users', string='Approved By',
                                          readonly=True,
                                          help='User who approved the requisition.')
    rejected_user_id = fields.Many2one('res.users', string='Rejected By',
                                       readonly=True,
                                       help='user who rejected the requisition')
    confirmed_date = fields.Date(string='Confirmed Date', readonly=True,
                                 help='Date of Requisition Confirmation')
    department_approval_date = fields.Date(string='Work Location Approval Date',
                                           readonly=True,
                                           help='Work Location Approval Date')
    approval_date = fields.Date(string='Approved Date', readonly=True,
                                help='Requisition Approval Date')
    reject_date = fields.Date(string='Rejection Date', readonly=True,
                              help='Requisition Rejected Date')
    source_location_id = fields.Many2one('stock.location',
                                         string='Source Location',
                                         help='Source location of requisition.')
    destination_location_id = fields.Many2one('stock.location',
                                              string="Destination Location",
                                              help='Destination location of requisition.')
    delivery_type_id = fields.Many2one('stock.picking.type',
                                       string='Delivery To',
                                       help='Type of Delivery.')
    internal_picking_id = fields.Many2one('stock.picking.type',
                                          string="Internal Picking")
    requisition_description = fields.Text(string="Reason For Requisition")
    purchase_count = fields.Integer(string='Purchase Count',
                                    help='Purchase Count',
                                    compute='_compute_purchase_count')
    internal_transfer_count = fields.Integer(string='Internal Transfer count',
                                             help='Internal Transfer count',compute='_compute_internal_transfer_count')


    work_location_id = fields.Many2one('hr.work.location', string='Work Location',
                              related='employee_id.work_location_id', store=True,
                              help='Work Location')

    manager_id = fields.Many2one('res.users', string='Location Manager',
                                 readonly=True, help='Location Manager')


    department_approval_date = fields.Date(string='Location Approval Date',
                                           readonly=True,
                                           help='Location Approval Date')





    state = fields.Selection(
        [('new', 'New'),
         ('waiting_department_approval', 'Waiting Work Location Approval'),
         ('waiting_head_approval', 'Waiting Head Approval'),
         ('approved', 'Approved'),
         ('purchase_order_created', 'Purchase Order Created'),
         ('received', 'Received'),
         ('cancelled', 'Cancelled')],
        default='new', copy=False, tracking=True)



    @api.model
    def create(self, vals):
        """generate purchase requisition sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'employee.purchase.requisition') or 'New'
        result = super(PurchaseRequisition, self).create(vals)
        return result

    def action_confirm_requisition(self):
        """confirm purchase requisition"""
        self.destination_location_id = self.employee_id.work_location_id.location_id.id

        # self.source_location_id = self.employee_id.department_id.department_location_id.id
        # self.destination_location_id = self.employee_id.employee_location_id.id
        self.delivery_type_id = self.destination_location_id.warehouse_id.in_type_id.id
        self.internal_picking_id = self.destination_location_id.warehouse_id.int_type_id.id
        self.write({'state': 'waiting_department_approval'})
        self.confirm_id = self.env.uid
        self.confirmed_date = fields.Date.today()


    # def action_confirm_requisition(self):
    #     """confirm purchase requisition"""

    #     result = super(PurchaseRequisition, self).action_confirm_requisition()

    #     self.source_location_id = self.employee_id.work_location_id.location_id.id
    #     self.destination_location_id = self.employee_id.employee_location_id.id


    #     return result


    def action_department_approval(self):
        """approval from department"""
        self.write({'state': 'waiting_head_approval'})
        self.manager_id = self.env.uid
        self.department_approval_date = fields.Date.today()

    def action_department_cancel(self):
        """cancellation from department """
        self.write({'state': 'cancelled'})
        self.rejected_user_id = self.env.uid
        self.reject_date = fields.Date.today()

    def action_head_approval(self):
        """approval from department head"""
        self.write({'state': 'approved'})
        self.requisition_head_id = self.env.uid
        self.approval_date = fields.Date.today()

    def action_head_cancel(self):
        """cancellation from department head"""
        self.write({'state': 'cancelled'})
        self.rejected_user_id = self.env.uid
        self.reject_date = fields.Date.today()

    def action_create_purchase_order(self):
        """create purchase order and internal transfer"""
        for rec in self.requisition_order_ids:
            if rec.requisition_type == 'internal_transfer':
                self.env['stock.picking'].create({
                    'location_id': self.source_location_id.id,
                    'location_dest_id': self.destination_location_id.id,
                    'picking_type_id': self.internal_picking_id.id,
                    'requisition_order': self.name,
                    'move_ids_without_package': [(0, 0, {
                        'name': rec.product_id.name,
                        'product_id': rec.product_id.id,
                        'product_uom': rec.product_id.uom_id,
                        'product_uom_qty': rec.product_qty,
                        'location_id': self.source_location_id.id,
                        'location_dest_id': self.destination_location_id.id,
                    })]
                })
            else:
                self.env['purchase.order'].create({
                    'partner_id': rec.partner_id.id,
                    'requisition_order': self.name,
                    "order_line": [(0, 0, {
                        'product_id': rec.product_id.id,
                        'product_qty': rec.product_qty,
                    })]})
        self.write({'state': 'purchase_order_created'})

    def _compute_internal_transfer_count(self):
        # self.internal_active = 0
        self.internal_transfer_count = self.env['stock.picking'].search_count([
            ('requisition_order', '=', self.name)])

    def _compute_purchase_count(self):
        self.purchase_count = self.env['purchase.order'].search_count([
            ('requisition_order', '=', self.name)])

    def action_receive(self):
        """receive purchase requisition"""
        self.write({'state': 'received'})
        self.receive_date = fields.Date.today()

    def get_purchase_order(self):
        """purchase order smart button view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('requisition_order', '=', self.name)],
        }

    def get_internal_transfer(self):
        """internal transfer smart tab view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfers',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('requisition_order', '=', self.name)],
        }

    def action_print_report(self):
        """print purchase requisition report"""
        data = {
            'employee': self.employee_id.name,
            'records': self.read(),
            'order_ids': self.requisition_order_ids.read(),
        }
        return self.env.ref(
            'prosys_purchase_requisition.action_report_purchase_requisition').report_action(
            self, data=data)



class RequisitionProducts(models.Model):
    _name = 'requisition.order'
    _description = 'Requisition order'

    requisition_product_id = fields.Many2one(
        'employee.purchase.requisition', help='Requisition product.')
    state = fields.Selection(string='State',
                             related='requisition_product_id.state')
    requisition_type = fields.Selection(
        string='Requisition Type',
        selection=[
            ('purchase_order', 'Purchase Order'),
            ('internal_transfer', 'Internal Transfer'),
        ], help='type of requisition')
    product_id = fields.Many2one('product.product', required=True,
                                 help='Product')
    description = fields.Text(
        string="Description",
        compute='_compute_name',
        store=True, readonly=False,
        precompute=True, help='Product Description')
    product_qty = fields.Integer(string='Quantity', help='Quantity')
    # product_uom = fields.Char(related='product_id.uom_id.name',
    #                   string='Unit of Measure', help='Product Uom')
    partner_id = fields.Many2one('res.partner', string='Vendor',
                                 help='Vendor for the requisition')

    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")




    qty_available = fields.Float("Available Qty", readonly=True, store=True,compute="get_qty")
    qty_foracast = fields.Float("Forecast Qty", readonly=True, store=True,compute="get_qty")
    move_ids = fields.One2many('stock.move', 'requisition_line_id', string='Reservation', readonly=True, copy=False)


    delay = fields.Float("Delay (Days)", readonly=True, group_operator="avg")

    cycle_time = fields.Float("Cycle Time (Days)", readonly=True, group_operator="avg")

    product_packaging_id = fields.Many2one('product.packaging', string='Packaging', domain="[('purchase', '=', True), ('product_id', '=', product_id)]", check_company=True,
                                           compute="_compute_product_packaging_id", store=True, readonly=False)
    product_packaging_qty = fields.Float('Packaging Quantity', compute="_compute_product_packaging_qty", store=True, readonly=False)


    @api.depends('product_id', 'product_qty', 'product_uom')
    def _compute_product_packaging_id(self):
        for line in self:
            # remove packaging if not match the product
            if line.product_packaging_id.product_id != line.product_id:
                line.product_packaging_id = False
            # suggest biggest suitable packaging
            if line.product_id and line.product_qty and line.product_uom:
                line.product_packaging_id = line.product_id.packaging_ids.filtered('purchase')._find_suitable_product_packaging(line.product_qty, line.product_uom) or line.product_packaging_id

    @api.onchange('product_packaging_id')
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id and self.product_qty:
            newqty = self.product_packaging_id._check_qty(self.product_qty, self.product_uom, "UP")
            if float_compare(newqty, self.product_qty, precision_rounding=self.product_uom.rounding) != 0:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            "This product is packaged by %(pack_size).2f %(pack_name)s. You should purchase %(quantity).2f %(unit)s.",
                            pack_size=self.product_packaging_id.qty,
                            pack_name=self.product_id.uom_id.name,
                            quantity=newqty,
                            unit=self.product_uom.name
                        ),
                    },
                }



    @api.depends('product_packaging_id', 'product_uom', 'product_qty')
    def _compute_product_packaging_qty(self):
        for line in self:
            if not line.product_packaging_id:
                line.product_packaging_qty = 0
            else:
                packaging_uom = line.product_packaging_id.product_uom_id
                packaging_uom_qty = line.product_uom._compute_quantity(line.product_qty, packaging_uom)
                line.product_packaging_qty = float_round(packaging_uom_qty / line.product_packaging_id.qty, precision_rounding=packaging_uom.rounding)




    @api.depends('product_packaging_qty')
    def _compute_product_qty(self):
        for line in self:
            if line.product_packaging_id:
                packaging_uom = line.product_packaging_id.product_uom_id
                qty_per_packaging = line.product_packaging_id.qty
                product_qty = packaging_uom._compute_quantity(line.product_packaging_qty * qty_per_packaging, line.product_uom)
                if float_compare(product_qty, line.product_qty, precision_rounding=line.product_uom.rounding) != 0:
                    line.product_qty = product_qty




    def _group_by(self):
        group_by_str = """
            sm.id,
            sm.reference,
            sm.picking_id,
            sm.state,
            sm.product_qty,
            sm.company_id,
            sp.name,
            sp.date_done,
            sp.creation_date,
            sp.scheduled_date,
            sp.partner_id,
            sp.is_backorder,
            sp.delay,
            sp.cycle_time,
            spt.code,
            spt.name,
            p.id,
            is_late,
            cat.id
        """

        return group_by_str
        
    def _select(self):
        select_str = """
            sm.id as id,
            sp.name as picking_name,
            sp.date_done as date_done,
            sp.creation_date as creation_date,
            sp.scheduled_date as scheduled_date,
            sp.partner_id as partner_id,
            sp.is_backorder as is_backorder,
            sp.delay as delay,
            sp.delay > 0 as is_late,
            sp.cycle_time as cycle_time,
            spt.code as picking_type_code,
            spt.name as operation_type,
            p.id as product_id,
            sm.reference as reference,
            sm.picking_id as picking_id,
            sm.state as state,
            sm.product_qty as product_qty,
            sm.company_id as company_id,
            cat.id as categ_id
        """

        return select_str

                                

    @api.depends('product_id')
    def get_qty(self):
        for rec in self:
            stock_report=self.env['stock.report'].search([('product_id','=',rec.product_id.id)])
            #     ('order_id.state','=','purchase')])

            cycle=0.0
            delays=0.0
            average=0.0
            for line in stock_report:

                average
                cycle+=line.cycle_time
                delays+=line.delay

            # print("############################",qty)
            rec.cycle_time=cycle
            rec.delay=delays

            rec.qty_available = rec.product_id.qty_available
            rec.qty_foracast = rec.product_id.virtual_available





    def action_product_forecast_report(self):
        self.ensure_one()
        action = self.product_id.action_product_forecast_report()
        action['context'] = {
            'active_id': self.product_id.id,
            'active_model': 'product.product',
            'move_to_match_ids': self.move_ids.filtered(lambda m: m.product_id == self.product_id).ids,
            'purchase_line_to_match_id': self.id,
        }
        warehouse = self.requisition_product_id.delivery_type_id.warehouse_id
        if warehouse:
            action['context']['warehouse'] = warehouse.id
        return action





    @api.depends('product_id')
    def _compute_name(self):
        """compute product description"""
        for option in self:
            if not option.product_id:
                continue
            product_lang = option.product_id.with_context(
                lang=self.requisition_product_id.employee_id.lang)
            option.description = product_lang.get_product_multiline_description_sale()

    @api.onchange('requisition_type')
    def _onchange_product(self):
        """fetching product vendors"""
        vendors_list = []
        for data in self.product_id.seller_ids:
            vendors_list.append(data.partner_id.id)
        return {'domain': {'partner_id': [('id', 'in', vendors_list)]}}
