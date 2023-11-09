from odoo import models, fields, api, _

# class ProjectProject(models.Model):
#     _inherit = 'project.project'

#     members_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
#                                    'user_id', 'Project Members', help="""Project's
#                                members are users who can have access to
#                                the tasks related to this project."""
#                                    )
#     team_id = fields.Many2one('crm.team', "Project Team",)
#     @api.onchange('team_id')
#     def _get_team_members(self):
#         self.update({"members_ids": [(6, 0, self.team_id.team_members_ids.ids)]})


class ProjectTask(models.Model):
    _inherit = 'project.task'


    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')
    is_genrate_sale_line_id = fields.Boolean(string='Is Genrate', defult=True)

    


    def action_copy_task(self):
        partners = self.env["res.partner"].search([('sale_lines_id' ,'=',self.sale_lines_id.id)])
        for customer in partners:
            print("ddddddddddddddddddddddddddddddddddddddd",customer.name)
            if customer.id ==self.partner_id.id:
                continue
            duplicated_task = self.copy()
            duplicated_task.partner_id = customer.id
            duplicated_task.is_genrate_sale_line_id = True
            duplicated_task.name = self.name
            if customer.user_id:
                duplicated_task.user_ids = [customer.user_id.id]



        self.is_genrate_sale_line_id = True


    












    # def _get_sale_lines(self):
    #     default_project =self.env.context.get('default_project_id', False)
    #     if not default_project:
    #         return
    #     else :
    #         project=self.env['project.project'].search([('id', '=', default_project)])
    #         return project.members_ids

    # def action_copy_task(self):
    #      for rec in self.partner_id.sale_lines_id:
    #         partner = []
            

    #         task_vals = {
    #             'project_id': self.project_id.id,
    #             'name': self.name,
    #             'planned_date_begin': self.date_from,
    #             'planned_date_end': self.date_to,
    #             'recurring_task': self.recurring_task,
    #         }
    #         created_task = self.env['project.task'].copy(task_vals)





#     def action_add_project_task(self):
#         return {
#             'name': _("Add Task"),
#             'type': 'ir.actions.act_window',
#             'res_model': 'add.tasks.wizard',
#             'view_mode': 'form',
#             'view_type': 'form',
#             'context': {
#                 'default_task_move_ids': self.ids,
#             },
#             'target': 'new',
#         }

# class AddTasksWizard(models.TransientModel):
#     _name = 'add.tasks.wizard'

#     project_id = fields.Many2one('project.project', string="Project")
#     name = fields.Char("Task Title")
#     sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')
#     date_from = fields.Datetime("Date From")
#     date_to = fields.Datetime("Date To")
#     recurring_task = fields.Boolean(string="Recurring Task")
#     partner_id = fields.Many2one('res.partner', string='Customer')





    # def add_sale_task(self):

    #      for rec in self.partner_id.sale_lines_id:
    #         print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",rec)
    #         partner = []
            

    #         task_vals = {
    #             'project_id': self.project_id.id,
    #             'name': self.name,
    #             'planned_date_begin': self.date_from,
    #             'planned_date_end': self.date_to,
    #             'recurring_task': self.recurring_task,
    #         }
    #         created_task = self.env['project.task'].create(task_vals)

    #         user_ids = self.project_id.sale_lines_id.ids
    #         created_task.write()

    #         return {'type': 'ir.actions.act_window_close'}
