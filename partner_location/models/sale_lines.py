from odoo import models, fields, api, tools

class SaleLines(models.Model):
    _inherit = 'res.partner'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')


class SaleLines(models.Model):
    _name = 'sale.lines'

    name = fields.Char(String="Sale Lins" ,translate=True)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')


class FieldServices(models.Model):
    _inherit = 'project.task'

    sale_lines_id = fields.Many2one('sale.lines', related='partner_id.sale_lines_id' ,string='Sale Lines')
    google_map_link_id = fields.Char(string='Google Map Link' ,compute="calculate_map_link_task")
    in_latitude = fields.Char("Latitude ")
    in_longitude = fields.Char("Longitude ")
    is_current_location = fields.Boolean(string="is this current Location", defult=False)


    @api.depends('in_latitude','in_longitude','is_current_location')
    def calculate_map_link_task(self):
        for rec in self:
            rec.google_map_link_id = "http://maps.google.com/maps?q="+str(rec.in_latitude)+ "," +str(rec.in_longitude)
            if rec.in_latitude and rec.in_longitude:
                rec.is_current_location = True

   








   

