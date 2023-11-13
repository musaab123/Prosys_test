from odoo import models, fields,  exceptions, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import geopy.distance


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')
    is_genrate_sale_line_id = fields.Boolean(string='Is Genrate', defult=True)

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


