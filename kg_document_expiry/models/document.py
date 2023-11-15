# -*- coding: utf-8 -*-
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields
from datetime import datetime, date, timedelta



class DocumentsDocument(models.Model):
    _inherit = 'documents.document'
    
    expiry_date = fields.Date('Expiry Date', tracking=True, default=fields.Date.today() + relativedelta(years=1))
    notify_before = fields.Integer('Notify Before', tracking=True)

    def mail_reminder(self):
        date_now = date.today() + timedelta(days=1)
        match = self.search([])
        print('Match >>>>>>>>>>>>>', match)
        for i in match:
            if i.expiry_date:
                # exp_date = i.expiry_date - timedelta(days=i.notify_before)
                exp_date = i.expiry_date - timedelta(days=7)

                print('Exp Date >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', exp_date)

                if date_now >= exp_date:
                    template_id = self.env.ref('kg_document_expiry.notify_document_expire_email')
                    template_id.send(i.id, force_send=True)


    # def mail_reminder(self):
    #     now = datetime.now() + timedelta(days=1)
    #     date_now = now.date()
    #     match = self.search([])
    #     for doc in match:
    #         if doc.expiry_date:
    #             exp_date = doc.expiry_date - timedelta(days=7)
    #             if date_now >= exp_date:
    #                 mail_content = "  Hello  " + str(doc.employee_ref.name) + ",<br>Your Document " + str(doc.name) + "is going to expire on " + \
    #                                str(doc.expiry_date) + ". Please renew it before expiry date"
    #                 main_content = {
    #                     'subject': _('Document-%s Expired On %s') % (str(doc.name),  str(doc.expiry_date)),
    #                     'author_id': self.env.user.partner_id.id,
    #                     'body_html': mail_content,
    #                     'email_to': doc.employee_ref.work_email,
    #                 }
    #                 self.env['mail.mail'].create(main_content).send()