from odoo import fields, models, api, _

class AccountMove(models.Model):
    _inherit = 'stock.move'

    def action_add_customer_task(self):
        return {
            'name': _("Set Task"),
            'type': 'ir.actions.act_window',
            'res_model': 'add.task.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_task_move_ids': self.ids,
            },
            'target': 'new',
        }
    
class ProjectProject(models.Model):
    _inherit = 'project.project'

    members_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                                   'user_id', 'Project Members', help="""Project's
                               members are users who can have access to
                               the tasks related to this project."""
                                   )
    team_id = fields.Many2one('crm.team', "Project Team",)
    @api.onchange('team_id')
    def _get_team_members(self):
        self.update({"members_ids": [(6, 0, self.team_id.team_members_ids.ids)]})
    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    team_id = fields.Many2one('crm.team', string="Project Team")

    def _get_team_members(self):
        default_project =self.env.context.get('default_project_id', False)
        if not default_project:
            return
        else :
            project=self.env['project.project'].search([('id', '=', default_project)])
            return project.members_ids

    available_user_ids = fields.Many2many(related='project_id.members_ids')
    user_ids = fields.Many2many('res.users', relation='project_task_user_rel', column1='task_id', column2='user_id',
        string='Assignees', default=_get_team_members , domain="[('id', 'in', available_user_ids)]" , context={'active_test': False}, tracking=True)


class AddProjectWizard(models.TransientModel):
    _name = 'add.task.wizard'

    project_id = fields.Many2one('project.project', string="Project")
    team_id = fields.Many2one('crm.team', "Project Team")
    name = fields.Char("Task Title")

    def set_task(self):
        task_move_ids = self.env.context.get('default_task_move_ids')
        if task_move_ids:
            for move in self.env['stock.move'].browse(task_move_ids):
                task_vals = {
                    'project_id': self.project_id.id,
                    'team_id': self.team_id.id,
                    'name': self.name,
                }
                created_task = self.env['project.task'].create(task_vals)

                # Update the project's team_id with the selected team
                self.project_id.write({'team_id': self.team_id.id})

                # Set the user_ids field based on team members
                user_ids = self.team_id.team_members_ids.ids

                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",user_ids)

                created_task.write({'user_ids': [(6, 0, user_ids)]})

        return {'type': 'ir.actions.act_window_close'}


# class AddProjectWizard(models.TransientModel):
#     _name = 'add.task.wizard'

#     project_id = fields.Many2one('project.project', string="Project")
#     team_id = fields.Many2one('crm.team', "Project Team")
#     name = fields.Char("Task Title")

#     def set_task(self):
#         task_move_ids = self.env.context.get('default_task_move_ids')
#         if task_move_ids:
#             for move in self.env['stock.move'].browse(task_move_ids):
#                 task_vals = {
#                     'project_id': self.project_id.id,
#                     'team_id': self.team_id.id,
#                     'name': self.name,
#                 }
#                 created_task = self.env['project.task'].create(task_vals)

#                 # Update the project's team_id with the selected team
#                 self.project_id.write({'team_id': self.team_id.id})

#                 # Set the user_ids field based on team members
#                 user_ids = self.team_id.team_members_ids.mapped('user_id').ids
#                 created_task.write({'user_ids': [(6, 0, user_ids)]})

#         return {'type': 'ir.actions.act_window_close'}



# class AddProjectWizard(models.TransientModel):
#     _name = 'add.task.wizard'

#     project_id = fields.Many2one('project.project', string="Project")
#     team_id = fields.Many2one('crm.team', "Project Team")
#     name = fields.Char("Task Title")

#     def set_task(self):
#         task_move_ids = self.env.context.get('default_task_move_ids')
#         if task_move_ids:
#             for move in self.env['stock.move'].browse(task_move_ids):
#                 task_vals = {
#                     'project_id': self.project_id.id,
#                     'team_id': self.team_id.id,
#                     'name': self.name,
#                 }
#                 # Create a new task in the selected project.
#                 created_task = self.env['project.task'].create(task_vals)

#                 # Update the project's team_id with the selected team
#                 self.project_id.write({'team_id': self.team_id.id})

#         return {'type': 'ir.actions.act_window_close'}
       

# class AddProjectWizard(models.TransientModel):
#     _name = 'add.task.wizard'

#     project_id = fields.Many2one('project.project', string="Project")
#     team_id = fields.Many2one('crm.team', "Project Team")
#     name = fields.Char("Task Title")

#     def set_task(self):
#         task_move_ids = self.env.context.get('default_task_move_ids')
#         if task_move_ids:
#             for move in self.env['stock.move'].browse(task_move_ids):
#                 task_vals = {
#                     'project_id': self.project_id.id,
#                     'team_id': self.project_id.team_id.id,
#                     'name': self.name,
#                 }
#                 print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",task_vals)
#                 # Create a new task in the selected project.
#                 self.env['project.task'].create(task_vals)
#         return {'type': 'ir.actions.act_window_close'}


# from odoo import fields, models, api, _


# class AccountMove(models.Model):
#     _inherit = 'stock.move'

#     def action_add_customer_task(self):
#         list_ids = []
#         for rec in self:
#             list_ids.append(rec.id)

#         return {
#             'name': _("Set Task"),
#             'type': 'ir.actions.act_window',
#             'res_model': 'add.task.wizard',
#             'view_mode': 'form,tree',
#             'view_type': 'form',
#             'context': {'default_tasks_ids': list_ids},
#             'target': 'new',
#         }


# class AddProjectWizard(models.TransientModel):
#     _name = 'add.task.wizard'

#     project_id = fields.Many2one('project.project', string="Project")
#     team_id = fields.Many2one('crm.team', "Project Team")
#     name = fields.Char("Task Title")

#     def set_task(self):

#         list_ids = self.env.context.get('default_tasks_ids')
#         operation_id = self.env['stock.move']
#         if self.env.context.get('default_tasks_ids'):
#             operation_id = self.env['stock.move'].search([('id', 'in', list_ids)])

#         for rec in operation_id:
#             rec.write(
#                 {
#                     'project_id': self.project_id.id,
#                     'team_id': self.team_id.id,
#                     'name': self.name,


#                 }
#             )