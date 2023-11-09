# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Midilaj (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

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

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')








   

