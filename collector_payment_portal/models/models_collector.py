# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import format_date, formatLang


class ResUser(models.Model):

	_inherit="res.users"
	
	collecter_id=fields.Many2one("res.users",string="Cash Collecters")

	# collecter_ids=fields.Many2many(related="partner_id.collecter_ids")
     

     
      
    
        


