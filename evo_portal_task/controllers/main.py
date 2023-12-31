from collections import OrderedDict
from operator import itemgetter
from markupsafe import Markup

from odoo import conf, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR, AND



class ProjectCustomerPortal(CustomerPortal):



    @http.route(['/my/tasks/documents/<model("project.task"):task_id>'], type='http', auth="user", website=True)
    def get_tasks_documents(self, task_id, **kw):
        document_object = request.env['ir.attachment']
        documents = document_object.sudo().search([('res_id', '=', task_id.id)])
        #make documents public so that portal users can access them
        if documents:
            for doc in documents:
                if not doc.public:
                    doc.write(
                        {
                            'public': True,
                        }
                    )

        page_name = 'my_tasks_docs'
        vals = {'documents': documents, 'page_name': page_name, 'task_id': task_id}
        return http.request.render('evo_portal_task.my_tasks_documents_template_id', vals)

        

    @http.route(['/task/change_stage_task'], type='http', auth="user", website=True)
    def portalchange_stage_task(self, **kw):
        if 'user_id' in kw:
            user_id = request.env['res.users'].sudo().browse(int(kw['user_id']))
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', user_id.id)])

        if 'task_id' in kw and not 'user_id' in kw:
            task_id = request.env['project.task'].sudo().browse(int(kw['task_id']))
            if task_id:
                if 'stage_id' in kw:
                    task_id.stage_id = int(kw['stage_id'])
            access_token = None
            task_sudo = self._document_check_access('project.task', task_id.id, access_token)
            values = self._task_get_page_view_values(task_sudo, access_token, **kw)
            return request.render("project.portal_my_task", values)
        
        elif 'timesheet_description' in kw:
            task_id = request.env['project.task'].sudo().browse(int(kw['task_id']))
            timesheet_date = kw['timesheet_date']

            # Check if a timesheet entry already exists for the same task and date
            existing_timesheet = request.env['account.analytic.line'].sudo().search([
                ('task_id', '=', task_id.id),
                ('date', '=', timesheet_date),
            ])

            if existing_timesheet:
                # Update the existing timesheet entry
                existing_timesheet.write({
                    'name': kw['timesheet_description'],
                    'unit_amount': float(kw['timesheet_time']),
                })
            else:
                # Create a new timesheet entry
                timesheet_id = request.env['account.analytic.line'].sudo().create({
                    'task_id': task_id.id,
                    'date': timesheet_date,
                    'employee_id': employee_id.id,
                    'name': kw['timesheet_description'],
                    'unit_amount': float(kw['timesheet_time']),
                })

            access_token = None
            task_sudo = self._document_check_access('project.task', int(kw['task_id']), access_token)
            values = self._task_get_page_view_values(task_sudo, access_token, **kw)
            return request.render("project.portal_my_task", values)
        else:
            pass

