# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import http, _
from operator import itemgetter
from pytz import timezone, UTC
from odoo.addons.resource.models.resource import float_to_time
from collections import OrderedDict
from collections import namedtuple
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime
from odoo.tools import groupby as groupbyelem

DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')


class PortalQR(http.Controller):

    @http.route(['/view/productlist'], type='http', auth="public", website=True)
    def portal_prodctlist(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby=None, **kw):
        qr_record = request.env['qr.generator.model'].sudo().search([])
        return request.render("portal_qr_gen.show_qr_productlist_screen", {
            'qr_record': qr_record,
            'page_name': 'qr_productlist_screen'
        })