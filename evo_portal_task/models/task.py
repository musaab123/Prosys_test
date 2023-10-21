from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    members_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                                   'user_id', 'Project Members', help="""Project's
                               members are users who can have access to
                               the tasks related to this project."""
                                   )
    team_id = fields.Many2one('crm.team', "Project Team",
                              
                             )

    @api.onchange('team_id')
    def _get_team_members(self):
        self.update({"members_ids": [(6, 0, self.team_id.team_members_ids.ids)]})

class Task(models.Model):
    _inherit = 'project.task'
    

    # freelancer_ids = fields.Many2many('res.users', string='Freelancer')
    # freelancer_ids = fields.Many2many(related='project_id.members_ids' ,string='Freelancer' )

    portal_task_type_ids = fields.Many2many('project.task.type', string='Portal Task Type',
                                            compute='compute_portal_task_type')
    assigned_customer_ids = fields.Many2many('res.partner', string='Assigned Customers')
    # customer_description = fields.Html(string='Customer Comments')


    def _get_team_members(self):
        default_project =self.env.context.get('default_project_id', False)
        if not default_project:
            return
        else :
            project=self.env['project.project'].search([('id', '=', default_project)])
            # return [(6, 0, project.members_ids.ids)]
            # self.available_user_ids = project.members_ids.ids
            return project.members_ids

    available_user_ids = fields.Many2many(related='project_id.members_ids')
    user_ids = fields.Many2many('res.users', relation='project_task_user_rel', column1='task_id', column2='user_id',
        string='Assignees', default=_get_team_members , domain="[('id', 'in', available_user_ids)]" , context={'active_test': False}, tracking=True)

        

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

    # @api.model
    # def create(self, values):
    #     res = super(Task, self).create(values)
    #     if res.freelancer_ids:
    #         for freelancer in res.freelancer_ids:
    #             follower_id = self.env['mail.followers'].sudo().create({
    #                 'res_id': res.id,
    #                 'partner_id': freelancer.partner_id.id,
    #                 'res_model': self._name,
    #             })
    #     return res

    # def write(self, values):
    #     if 'freelancer_ids' in values:
    #         freelancer_ids = self.env['res.users'].search([('id', 'in', values['freelancer_ids'][0][2])])
    #         for freelancer in freelancer_ids:
    #             follower_id = self.env['mail.followers'].sudo().search(
    #                 [('res_id', '=', self.id), ('partner_id', '=', freelancer.partner_id.id),
    #                  ('res_model', '=', self._name)])
    #             if not follower_id:
    #                 follower_id = self.env['mail.followers'].sudo().create({
    #                     'res_id': self.id,
    #                     'partner_id': freelancer.partner_id.id,
    #                     'res_model': self._name,
    #                 })
    #     return super(Task, self).write(values)