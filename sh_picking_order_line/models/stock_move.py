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
    # description = fields.Html(translate=True)

    @api.onchange('team_id')
    def _get_team_members(self):
        self.update({"members_ids": [(6, 0, self.team_id.team_members_ids.ids)]})
    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    team_id = fields.Many2one('crm.team', string="Project Team")
    description = fields.Text(string="Description", translate=True)

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
    date_deadline = fields.Date("Deadline")
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', store=True,)
    location_id = fields.Many2one('stock.location', 'Source Location', auto_join=True, index=True  ,domain=[('usage', '=', 'internal')])
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', auto_join=True, index=True ,domain=[('usage', '=', 'internal')])
    picking_type_code = fields.Selection(related='picking_type_id.code', readonly=True)
    is_internal_picking = fields.Boolean(compute='_compute_is_internal_picking')

    @api.depends('picking_type_id.code')
    def _compute_is_internal_picking(self):
        for move in self:
            move.is_internal_picking = move.picking_type_id.code == 'internal'


    def set_task(self):
        task_move_ids = self.env.context.get('default_task_move_ids')
        total_quantity = 0  # Initialize a variable to store the total quantity
        description = ""

        for move in self.env['stock.move'].browse(task_move_ids):
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooo",move)
            if move.picking_type_id.code == 'incoming':
                description = f"From source location 'vendor' to destination location 'WH/Stock' "
                description += f"for product '{move.product_id.name}' with quantity {total_quantity + move.product_uom_qty}."
                total_quantity += move.product_uom_qty  

            elif move.picking_type_id.code == 'internal':
                description = f"From source location '{self.location_id.name}' to destination location '{self.location_dest_id.name}' "
                description += f"for product '{move.product_id.name}' with quantity {total_quantity + move.product_uom_qty}."
                total_quantity += move.product_uom_qty 
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",{move.location_id}) 


            elif move.picking_type_id.code == 'outgoing':
                description = f"From source location 'Customer' to destination location  'WH/Stock' "
                description += f"for product '{move.product_id.name}' with quantity {total_quantity + move.product_uom_qty}."
                total_quantity += move.product_uom_qty

            else:
                description = f"From source location 'Customer/vindor' to destination location  'WH/Stock' "
                description += f"for product '{move.product_id.name}' with quantity {total_quantity + move.product_uom_qty}."
                total_quantity += move.product_uom_qty

            

        task_vals = {
            'project_id': self.project_id.id,
            'team_id': self.team_id.id,
            'name': self.name,
            'date_deadline': self.date_deadline,
            'description': description,
        }
        created_task = self.env['project.task'].create(task_vals)

        self.project_id.write({'team_id': self.team_id.id})

        user_ids = self.team_id.team_members_ids.ids
        created_task.write({'user_ids': [(6, 0, user_ids)]})

        return {'type': 'ir.actions.act_window_close', 'context': {'default_description': description, 'default_total_quantity': total_quantity}}

   