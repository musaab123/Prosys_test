# Part of Softhealer Technologies.
from odoo import models, fields,  exceptions, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

import geopy.distance


class ProjectTask(models.Model):
    _inherit = 'project.task'


    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')
    is_genrate_sale_line_id = fields.Boolean(string='Is Genrate', defult=True)

    # def action_fsm_validate(self, stop_running_timers=False):
    #     for task in self:
    #         partner = task.partner_id

    #         # Assuming user_ids is a Many2one field pointing to res.users
    #         assigned_user = task.user_ids
    #         print("Salesperson Latitude:", assigned_user)


    #         salesperson_partner = assigned_user.partner_id
    #         print("partner Latitude:", salesperson_partner.partner_latitude)

    #         # user_latitude = float(salesperson_partner.partner_latitude)
    #         # user_longitude = float(salesperson_partner.partner_longitude)
    #         # print("Salesperson Latitude:", user_latitude)
    #         # print("Salesperson Longitude:", user_longitude)

    #         if not partner:
    #             continue

    #         config_distance = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))

    #         print("Customer Latitude:", partner.partner_latitude)
    #         print("Customer Longitude:", partner.partner_longitude)

    #         distance = geopy.distance.geodesic(
    #             (partner.partner_latitude, partner.partner_longitude),(0,0)
    #         ).meters

    #         print("Distance:", distance)

    #         if config_distance and distance >= config_distance:
    #             raise UserError("You can't complete this task because you are not in the desired location!")

    #     return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)


    # def action_fsm_validate(self, stop_running_timers=False):
    #     for task in self:
    #         partner = task.partner_id
    #         user = task.user_id  # Assuming user_id is a Many2one field pointing to res.users

    #         if not partner or not user or not user.partner_id:
    #             continue

    #         # Access the related partner record of the Salesperson
    #         salesperson_partner = user.partner_id

    #         user_latitude = float(salesperson_partner.partner_latitude)
    #         user_longitude = float(salesperson_partner.partner_longitude)
    #         print("Salesperson Latitude:", user_latitude)
    #         print("Salesperson Longitude:", user_longitude)

    #         config_distance = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))

    #         print("Customer Latitude:", partner.partner_latitude)
    #         print("Customer Longitude:", partner.partner_longitude)

    #         distance = geopy.distance.geodesic(
    #             (partner.partner_latitude, partner.partner_longitude),
    #             (user_latitude, user_longitude)
    #         ).meters

    #         print("Distance:", distance)

    #         if config_distance and distance >= config_distance:
    #             raise UserError("You can't complete this task because you are not in the desired location!")

    #     return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)


    def action_fsm_validate(self, stop_running_timers=False):
        for task in self:
            partner = task.partner_id

            if not partner or not task:
                continue

            user_latitude = float(task.in_latitude)
            user_longitude = float(task.in_longitude)
            print("task Latitude:", user_latitude)
            print("task Longitude:", user_longitude)

            distance_id = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))

            print("Customer Latitude:", partner.partner_latitude)
            print("Customer Longitude:", partner.partner_longitude)
            print("distance_id:", distance_id)


            distance = geopy.distance.geodesic(
                (partner.partner_latitude, partner.partner_longitude),
                (user_latitude, user_longitude)
            ).meters

            if distance_id:
                print('if distance_id and if distance',distance ,distance_id)
                if distance >= distance_id:
                    print('comperson between distance and distance_id',distance ,distance_id)
                    raise ValidationError(_("You Can't Confirm this Task Because Of The Following Reasons:\n"
                        "You are Not In The Right Location OF the Customer ({}) You can Only Confirm Task In Customer Location"
                        ).format(task.partner_id.name))

        return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)




    # def action_fsm_validate(self, stop_running_timers=False):
       

    #     for task in self:
    #         partner = task.partner_id
    #         task_sdn = task.partner_id.user_id
    #         # print("Salesperson name:", task_sdn.name)


    #         user_latitude = float(task_sdn.partner_latitude)
    #         user_longitude = float(task_sdn.partner_longitude)
    #         print("Salesperson Latitude:", user_latitude)
    #         print("Salesperson Longitude:", user_longitude)
            
    #         if not partner or not task_sdn or not task_sdn.partner_id:
    #             continue

    #         distance_id = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))

    #         print("Customer Latitude:", partner.partner_latitude)
    #         print("Customer Longitude:", partner.partner_longitude)
    #         print("Salesperson Latitude:", user_latitude)
    #         print("Salesperson Longitude:", user_longitude)

    #         # Calculate the distance between the customer and the salesperson
    #         distance = geopy.distance.geodesic(
    #             (partner.partner_latitude, partner.partner_longitude),
    #             (user_latitude, user_longitude)
    #         ).meters

    #         print("Distance:", distance)

    #         if config_distance and distance >= config_distance:
    #             raise UserError("You can't complete this task because you are not in the desired location!")

    #     return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)

   

    # def action_fsm_validate(self, stop_running_timers=False):
    #     for task in self:
    #         partner = task.partner_id
    #         task = task.partner_id.user_id
    #         print("partner longitude",task)


    #         if not partner or not task.user_id:
    #             continue

    #         config_distance = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))

    #         # Calculate the distance between the customer and the salesperson
    #         distance = geopy.distance.geodesic(
    #             (partner.partner_latitude, partner.partner_longitude),
    #             (task.partner_latitude, task.partner_longitude)
    #         ).meters

    #         print("partner latitude",task.partner_latitude)
    #         print("partner longitude",task.partner_longitude)
    #         print("partner longitude",distance)



    #         if config_distance:
    #                print('if config_distance and if distance',distance ,config_distance)
    #                if distance >= config_distance:
    #                    print('comperson between distance and config_distance',distance ,config_distance)
    #                raise UserError("You Can't  complete this task because you are not in the desired location!!!")
    #     return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)

    # def action_fsm_validate(self, stop_running_timers=False):
    #     for task in self:
    #         partner = task.partner_id
    #         print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",partner.name)

    #         if not partner:
    #             continue

    #         config_distance = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))
    #         print("configration distance : ",config_distance)

    #         distance = geopy.distance.geodesic((partner.partner_latitude,partner.partner_longitude), (partner.partner_latitude,partner.partner_longitude)).meters
    #         print("distance",distance)
    #         print("partner latitude",partner.partner_latitude)
    #         print("partner longitude",partner.partner_longitude)

    #         if config_distance:
    #                 print('if config_distance and if distance',distance ,config_distance)
    #                 if distance >= config_distance:
    #                     print('comperson between distance and config_distance',distance ,config_distance)
    #                     raise UserError("You Can't  complete this task because you are not in the desired location!!!")
    #     return super(ProjectTask, self).action_fsm_validate(stop_running_timers=stop_running_timers)

    # def action_fsm_validate(self, stop_running_timers=False ):
    #     partner_id = self.sudo()
    #     print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    #     config_distance = float(self.env["ir.config_parameter"].sudo().get_param("partner_location_distance_id"))
    #     print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj",config_distance)
    #     distance = geopy.distance.geodesic( (partner_id.partner_longitude,partner_id.partner_latitude),).meters
    #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",distance)

    #     if config_distance:
    #                 print('config_distance condition',distance ,config_distance)

    #                 if distance >= config_distance:
    #                     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',distance ,config_distance)
    #                     raise UserError("You Can't Check In,Please Try Again Later !!!")
    #     return super(ProjectTask, self).action_fsm_validate()

    


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
