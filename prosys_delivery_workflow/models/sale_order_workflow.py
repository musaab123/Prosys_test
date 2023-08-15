from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'stock.picking'

    # state = fields.Selection(
    #     selection=[
    #         ('draft', "Quotation"),
    #         ('sent', "Quotation Sent"),
    #         ('customer_appr', "Waiting Salesperson Approve"),
    #         ('salesman_appr', "Waiting Manager Approve"),
    #         ('manager_appr', "Waiting CEO Approve"),
    #         ('sale', "CEO Approved"),
    #         ('done', "Locked"),
    #         ('cancel', "Cancelled"),
    #     ],
    #     string="Status",
    #     readonly=True, copy=False, index=True,
    #     tracking=3,
    #     default='draft')

    # def status_to_customer_appr(self):
    #     ''' Quotation -> Customer Approve '''
    #     self.state = 'customer_appr'
    #     self.send_notification_message()

    # def status_to_salesman_appr(self):
    #     ''' Customer Approve -> Salesperson Approve '''
    #     self.state = 'salesman_appr'
    #     self.send_notification_message()

    # def status_to_manager_appr(self):
    #     ''' Salesperson Approve -> Manager Approve '''
    #     self.state = 'manager_appr'
    #     self.send_notification_message()

    # def send_notification_message(self):
      
    #     user_id_list = []
    #     notification_ids = []
    #     if self.state == 'customer_appr':
    #         result = self.env['res.users'].search([])
    #         for rec in result:
    #             if rec.user_has_groups('prosys_so_po_workflow.group_workflow_saleperson_approve'):
    #                 user_id_list.append(rec.partner_id.id)
    #         for rec in user_id_list:
    #             notification_ids.append((0, 0, {
    #                 'res_partner_id': rec,
    #                 'notification_type': 'inbox'}))

    #     elif self.state == 'salesman_appr':
    #         result = self.env['res.users'].search([])
    #         for rec in result:
    #             if rec.user_has_groups('prosys_so_po_workflow.group_workflow_manager_approve'):
    #                 user_id_list.append(rec.partner_id.id)
    #         for rec in user_id_list:
    #             notification_ids.append((0, 0, {
    #                 'res_partner_id': rec,
    #                 'notification_type': 'inbox'}))

    #     elif self.state == 'manager_appr':
    #         result = self.env['res.users'].search([])
    #         for rec in result:
    #             if rec.user_has_groups('prosys_so_po_workflow.group_workflow_ceo_approve'):
    #                 user_id_list.append(rec.partner_id.id)
    #         for rec in user_id_list:
    #             notification_ids.append((0, 0, {
    #                 'res_partner_id': rec,
    #                 'notification_type': 'inbox'}))

    #     self.message_post(body='Need your confirmation please!!', message_type='notification',
    #                               author_id=self.create_uid.partner_id.id, notification_ids=notification_ids)


