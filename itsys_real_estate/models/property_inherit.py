from odoo import api, fields, models

class building_unit_inherit(models.Model):
    _inherit = "building"

    build_number =fields.Char(" Build Number")
    branch_number =fields.Char(" Build Number")
    email_code =fields.Char(" Build Number")
    district =fields.Char(" Build Number")
    street_name =fields.Char(" Build Number")
    zip = fields.Char(change_default=True)



    instrument_number = fields.Integer("Deed Number")
    instrument_date= fields.Date('Deed Date')
    parking_number= fields.Integer('Number of Parking’s')
    agency_number = fields.Char("Legal Agency Number")
    agency_date = fields.Date("Legal Agency Date")
    agent_name= fields.Char('Agency Number')
    agent_phone= fields.Char('Agency Mobile Number (absher)')
    bulding_use= fields.Char('Real Estate Use')



