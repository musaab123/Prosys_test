from odoo import fields, models, api, _
class BuildingAc(models.Model):
    _name = 'building.ac'

    name = fields.Char('Ac Type', required=True)

  
class UnitBuildingAc(models.Model):
    _name = "building.ac.unit"
    _description = "building ac unit"

    ac_bulding_id = fields.Many2one('building.ac', string="Ac Type")
    # commitment_name = fields.Char(related="ac_bulding_id.name" , store=True,readonly=False)
    ac_number = fields.Char(String='Number')
    unit_id = fields.Many2one('product.template',ondelete='cascade')
  