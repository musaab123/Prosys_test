# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from markupsafe import escape, Markup
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_amount, format_date, formatLang, get_lang, groupby
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('employee_approve', 'Waiting Management Approve'),
        ('management_approve', 'Waiting CEO Approve'),
        ('purchase', 'CEO Approved'),
        ('on_hold', 'ON HOLD'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def status_to_employee_appr(self):
        ''' RFQ -> Employee Approve '''
        self.state = 'employee_approve'
        self.send_notification_message()

    def status_to_management_appr(self):
        ''' Employee Approve -> Management Approve '''
        self.state = 'management_approve'
        self.send_notification_message()

    def status_to_on_hold(self):
        ''' Management Approve -> ON HOLD '''
        self.state = 'on_hold'
        self.send_notification_message()

    def button_confirm(self):
        ''' Management Approve -> CEO APPROVE '''
        self.state = 'draft'
        res = super(PurchaseOrder, self).button_confirm()

        return res

    def send_notification_message(self):
        # context = self._context
        # current_uid = context.get('uid')
        # user_id = self.env['res.users'].browse(current_uid)
        user_id_list = []
        notification_ids = []
        if self.state == 'employee_approve':
            result = self.env['res.users'].search([])
            for rec in result:
                if rec.user_has_groups('prosys_so_po_workflow.purchase_group_workflow_manager_approve'):
                    user_id_list.append(rec.partner_id.id)
            for rec in user_id_list:
                notification_ids.append((0, 0, {
                    'res_partner_id': rec,
                    'notification_type': 'inbox'}))

        elif self.state == 'management_approve':
            result = self.env['res.users'].search([])
            for rec in result:
                if rec.user_has_groups('prosys_so_po_workflow.purchase_group_workflow_ceo_approve'):
                    user_id_list.append(rec.partner_id.id)
            for rec in user_id_list:
                notification_ids.append((0, 0, {
                    'res_partner_id': rec,
                    'notification_type': 'inbox'}))

        elif self.state == 'on_hold':
            result = self.env['res.users'].search([])
            for rec in result:
                if rec.user_has_groups('prosys_so_po_workflow.purchase_group_workflow_ceo_approve'):
                    user_id_list.append(rec.partner_id.id)
            for rec in user_id_list:
                notification_ids.append((0, 0, {
                    'res_partner_id': rec,
                    'notification_type': 'inbox'}))

        #post the message
        self.message_post(body='Need your confirmation please!!', message_type='notification',
                                  author_id=self.create_uid.partner_id.id, notification_ids=notification_ids)



