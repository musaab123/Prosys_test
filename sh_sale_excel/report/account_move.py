# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models
import xlwt
import base64
from io import BytesIO


class InvoiceExcelExtended(models.Model):
    _name = "invoice.extended"
    _description = 'Invoice Extended'

    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)


class SaleOrder(models.Model):
    _inherit = "account.move"

    def action_account_move_xls(self):

        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        row = 1

        final_value = {}
        active_ids = self.env.context.get('active_ids')

        for sale_order in self.env['account.move'].browse(active_ids):
            order_lines = []
            for lines in sale_order.invoice_line_ids:                 
                product = {
                    'product_id': lines.product_id.name,
                    'label': lines.name,
                    'quantity': lines.quantity,
                    'discount': lines.discount,
                    'price_unit': lines.price_unit,
                    'price_subtotal': lines.price_subtotal,
                }
                if lines.tax_ids:
                    taxes = []
                    for tax_ids in lines.tax_ids:
                        taxes.append(tax_ids.name)
                    product['tax_ids'] = taxes
                order_lines.append(product)
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",order_lines)
            final_value['partner_id'] = sale_order.partner_id.name
            final_value['name'] = sale_order.name
            final_value['invoice_date'] = sale_order.invoice_date
            final_value['invoice_date_due'] = sale_order.invoice_date_due
            final_value['l10n_sa_delivery_date'] = sale_order.l10n_sa_delivery_date
            final_value['currency_id'] = sale_order.currency_id
            final_value['invoice_payment_term_id'] = sale_order.invoice_payment_term_id


            
            
            final_value['payment_reference'] = sale_order.payment_reference
            final_value['state'] = dict(self.env['account.move'].fields_get(
                allfields=['state'])['state']['selection'])[sale_order.state]
            final_value['ref'] = sale_order.ref
            final_value['user_id'] = sale_order.user_id.name
            final_value['fiscal_position_id'] = sale_order.fiscal_position_id.name
            final_value['amount_untaxed'] = sale_order.amount_untaxed
            final_value['amount_tax'] = sale_order.amount_tax
            final_value['amount_total'] = sale_order.amount_total
            final_value['narration'] = sale_order.narration
        
            format1 = xlwt.easyxf('font:bold True;;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format7 = xlwt.easyxf('borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;')

            worksheet = workbook.add_sheet('name')

            worksheet.col(0).width = int(25*260)
            worksheet.col(1).width = int(25*260)
            worksheet.col(2).width = int(14*260)
            worksheet.col(3).width = int(16*260)
            worksheet.col(4).width = int(15*260)
            worksheet.col(5).width = int(14*260)
            worksheet.col(6).width = int(14*260)
            worksheet.col(7).width = int(14*260)
            worksheet.col(8).width = int(14*260)
            worksheet.col(9).width = int(14*260)
            worksheet.col(10).width = int(14*260)
            worksheet.col(11).width = int(14*260)



            if sale_order.state not in ['draft', 'sent']:
                heading_title = ""
                if sale_order.state in ['draft', 'sent']:
                    heading_title = "Quotation"

                else:
                    heading_title = "Invoice : "

                worksheet.write_merge(
                    0, 1, 0, 7, heading_title + final_value['name'], heading_format)

            elif sale_order.state in ['draft', 'sent']:
                worksheet.write_merge(
                    0, 1, 0, 7, 'Quotation : ' + final_value['name'], heading_format)
                worksheet.write(11, 0, 'Expiration Date', format1)
                if final_value['invoice_date']:
                    worksheet.write(11, 1, str(
                        final_value['invoice_date']), format3)

            worksheet.write(3, 0, "Customer", format1)
            worksheet.write(3, 1, final_value['partner_id'], format1)

            address = ""
            if sale_order.partner_id.street:
                address += sale_order.partner_id.street
            if sale_order.partner_id.street2:
                address += " "+sale_order.partner_id.street2
            if sale_order.partner_id.city:
                address += "\n"+sale_order.partner_id.city
            if sale_order.partner_id.state_id:
                address += " "+sale_order.partner_id.state_id.name
            if sale_order.partner_id.zip:
                address += " "+sale_order.partner_id.zip
            if sale_order.partner_id.country_id:
                address += "\n"+sale_order.partner_id.country_id.name
            if address:
                worksheet.write_merge(4, 6, 1, 2, address, format3)

            worksheet.write(7, 0, "ContactNo", format1)
            if sale_order.partner_id.phone:
                worksheet.write(7, 1, sale_order.partner_id.phone, format3)

            worksheet.write(8, 0, "Mobile", format1)
            if sale_order.partner_id.mobile:
                worksheet.write(8, 1, sale_order.partner_id.mobile, format3)

            worksheet.write(3, 3, 'Date', format1)
            worksheet.write_merge(3, 3, 4, 5, str(
                final_value['invoice_date_due']), format3)
            worksheet.write(4, 3, 'Payment Reference', format1)
            if final_value['payment_reference']:
                worksheet.write_merge(
                    4, 4, 4, 5, final_value['payment_reference'], format3)
            else:
                worksheet.write_merge(
                    4, 4, 4, 5, "No Payment Terms Defined", format3)
            worksheet.write(5, 3, 'Payment terms.', format1)
            if final_value['invoice_payment_term_id']:
                worksheet.write_merge(5, 5, 4, 5, str(
                    final_value['invoice_payment_term_id']), format3)
            else:
                worksheet.write_merge(
                    5, 5, 4, 5, "No Customer Reference Defined", format3)
            worksheet.write(6, 3, 'State', format1)
            worksheet.write_merge(6, 6, 4, 5, final_value['state'], format3)
            worksheet.write(8, 3, "SalesPerson", format1)
            if final_value['user_id']:
                worksheet.write_merge(
                    8, 8, 4, 5, final_value['user_id'], format3)
            worksheet.write(9, 3, "Source Document", format1)
            if final_value['ref']:
                worksheet.write_merge(
                    9, 9, 4, 5, final_value['ref'], format3)
            worksheet.write(10, 3, "Currency", format1)
            if final_value['currency_id']:
                worksheet.write_merge(
                    10, 10, 4, 5, sale_order.currency_id.name, format3)

            worksheet.write(13, 0, "Product", bold)
            worksheet.write(13, 1, "Label", bold)
            worksheet.write(13, 2, "Total Qty", bold)
            worksheet.write(13, 3, "Unit Price", bold)
            worksheet.write(13, 4, "Disc. (%)", bold)
            worksheet.write(13, 5, "Taxes", bold)
            worksheet.write(13, 6, "Subtotal", bold)

            row = 14

            for rec in order_lines:
                if rec.get('product_id'):
                    worksheet.write(row, 0, rec.get('product_id'), format3)
                if rec.get('label'):
                    worksheet.write(row, 1, rec.get('label'), format3)
                if rec.get('quantity'):
                    worksheet.write(row, 2, rec.get(
                        'quantity'), format4)
                if rec.get('price_unit'):
                    worksheet.write(row, 3, rec.get('price_unit'), format4)

                if rec.get('discount'):
                    worksheet.write(row, 4, rec.get('discount'), format4)

                if rec.get('tax_ids'):
                    worksheet.write(row, 5, ",".join(
                        rec.get('tax_ids')), format4)
                else:
                    worksheet.write(row, 6, '', format4)
                if final_value['currency_id'].position == "before":
                    worksheet.write(row, 6, rec.get('price_subtotal'), format4)
                else:
                    worksheet.write(row, 6, rec.get('price_subtotal'), format4)
                row += 1

            row += 2
            worksheet.write_merge(
                row, row, 5, 6, 'Total Without Taxes', format8)
            worksheet.write_merge(row+1, row+1, 5, 6, 'Taxes', format8)
            worksheet.write_merge(row+2, row+2, 5, 6, 'Total', format8)
            if final_value['currency_id'].position == "before":
                worksheet.write(
                    row, 7,  final_value['amount_untaxed'], format7)
                worksheet.write(row+1, 7, final_value['amount_tax'], format7)
                worksheet.write(row+2, 7, final_value['amount_total'], format7)
            else:
                worksheet.write(row, 7, final_value['amount_untaxed'], format7)
                worksheet.write(row+1, 7, final_value['amount_tax'], format7)
                worksheet.write(row+2, 7, final_value['amount_total'], format7)
            row += 4
            if final_value['narration']:
                worksheet.write_merge(
                    row, row+1, 0, 5, final_value['narration'], format3)

        filename = ('Invoice Xls Report' + '.xls')
        fp = BytesIO()
        workbook.save(fp)

        export_id = self.env['invoice.extended'].sudo().create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename,
        })

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=invoice.extended&field=excel_file&download=true&id=%s&filename=%s' % (export_id.id, export_id.file_name),
            'target': 'new',
        }
