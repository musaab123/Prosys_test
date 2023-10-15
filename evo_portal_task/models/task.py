from odoo import models, fields, api


class Task(models.Model):
    _inherit = 'project.task'

    freelancer_ids = fields.Many2many('res.users', string='Freelancer')
    portal_task_type_ids = fields.Many2many('project.task.type', string='Portal Task Type',
                                            compute='compute_portal_task_type')
    assigned_customer_ids = fields.Many2many('res.partner', string='Assigned Customers')
    customer_description = fields.Html(string='Customer Comments')

    @api.depends('stage_id', 'project_id')
    def compute_portal_task_type(self):
        for rec in self:
            if rec.project_id:
                stage_ids = self.env['project.task.type'].sudo().search([('project_ids', '=', rec.project_id.id)])
                if stage_ids:
                    rec.portal_task_type_ids = [(4, x.id) for x in stage_ids]
                else:
                    rec.portal_task_type_ids = False
            else:
                rec.portal_task_type_ids = False

    @api.model
    def create(self, values):
        res = super(Task, self).create(values)
        if res.freelancer_ids:
            # res['message_follower_ids']=[(4, record.id, None) for record in res.freelancer_ids]
            for freelancer in res.freelancer_ids:
                follower_id = self.env['mail.followers'].sudo().create({
                    'res_id': res.id,
                    'partner_id': freelancer.partner_id.id,
                    'res_model': self._name,
                })
        return res

    def write(self, values):
        if 'freelancer_ids' in values:
            freelancer_ids = self.env['res.users'].search([('id', 'in', values['freelancer_ids'][0][2])])
            for freelancer in freelancer_ids:
                follower_id = self.env['mail.followers'].sudo().search(
                    [('res_id', '=', self.id), ('partner_id', '=', freelancer.partner_id.id),
                     ('res_model', '=', self._name)])
                if not follower_id:
                    follower_id = self.env['mail.followers'].sudo().create({
                        'res_id': self.id,
                        'partner_id': freelancer.partner_id.id,
                        'res_model': self._name,
                    })
        return super(Task, self).write(values)