# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models
import xlwt
import base64
from io import BytesIO


class SaleExcelExtended(models.Model):
    _name = "purchase.extended"
    _description = 'Purchase Extended'

    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)


class SaleOrder(models.Model):
    _inherit = "purchase.order"

    def action_purchase_order_xls(self):

        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        row = 1

        final_value = {}
        active_ids = self.env.context.get('active_ids')

        for sale_order in self.env['purchase.order'].browse(active_ids):
            order_lines = []
            for lines in sale_order.order_line:                 
                product = {
                    'product_id': lines.product_id.name,
                    'description': lines.name,
                    'product_packaging_id':lines.product_packaging_id.name,
                    'test':lines.product_packaging_id.qty,
                    'product_packaging_qty':lines.product_packaging_qty,
                    'product_qty': lines.product_qty,
                    'product_uom': lines.product_uom.name,
                    'carton_price': lines.price_unit * lines.product_packaging_id.qty,
                    # 'discount': lines.discount,
                    'price_unit': lines.price_unit,
                    'price_subtotal': lines.price_subtotal,
                }
                if lines.taxes_id:
                    taxes = []
                    for taxes_id in lines.taxes_id:
                        taxes.append(taxes_id.name)
                    product['taxes_id'] = taxes
                order_lines.append(product)
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",order_lines)
            final_value['partner_id'] = sale_order.partner_id.name
            final_value['name'] = sale_order.name
            final_value['date_approve'] = sale_order.date_approve
            final_value['date_planned'] = sale_order.date_planned
            final_value['currency_id'] = sale_order.currency_id
            final_value['partner_ref'] = sale_order.partner_ref
            final_value['payment_term_id'] = sale_order.payment_term_id.name
            final_value['origin'] = sale_order.origin

            
            # final_value['partner_ref'] = sale_order.partner_ref
            final_value['state'] = dict(self.env['purchase.order'].fields_get(
                allfields=['state'])['state']['selection'])[sale_order.state]
            final_value['incoterm_id'] = sale_order.incoterm_id
            final_value['user_id'] = sale_order.user_id.name
            # final_value['pricelist_id'] = sale_order.pricelist_id.name
            final_value['fiscal_position_id'] = sale_order.fiscal_position_id.name
            final_value['amount_untaxed'] = sale_order.amount_untaxed
            final_value['amount_tax'] = sale_order.amount_tax
            final_value['amount_total'] = sale_order.amount_total
            final_value['notes'] = sale_order.notes
            
            # final_value['partner_invoice_id'] = sale_order.partner_invoice_id.name
            # final_value['partner_shipping_id'] = sale_order.partner_shipping_id.name

            format1 = xlwt.easyxf('font:bold True;;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format7 = xlwt.easyxf('borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;')

            worksheet = workbook.add_sheet(sale_order.name)

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
                    heading_title = "Purchase Order : "

                worksheet.write_merge(
                    0, 1, 0, 7, heading_title + final_value['name'], heading_format)

            elif sale_order.state in ['draft', 'sent']:
                worksheet.write_merge(
                    0, 1, 0, 7, 'Quotation : ' + final_value['name'], heading_format)
                worksheet.write(11, 0, 'Expiration Date', format1)
                if final_value['date_approve']:
                    worksheet.write(11, 1, str(
                        final_value['date_approve']), format3)

            worksheet.write(3, 0, "Vendor", format1)
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
                final_value['date_planned']), format3)
            worksheet.write(4, 3, 'Payment Term', format1)
            if final_value['payment_term_id']:
                worksheet.write_merge(
                    4, 4, 4, 5, final_value['payment_term_id'], format3)
            else:
                worksheet.write_merge(
                    4, 4, 4, 5, "No Payment Terms Defined", format3)
            worksheet.write(5, 3, 'Vendor Reference.', format1)
            if final_value['partner_ref']:
                worksheet.write_merge(5, 5, 4, 5, str(
                    final_value['partner_ref']), format3)
            else:
                worksheet.write_merge(
                    5, 5, 4, 5, "No Vendor Reference Defined", format3)
            worksheet.write(6, 3, 'State', format1)
            worksheet.write_merge(6, 6, 4, 5, final_value['state'], format3)
            # worksheet.write(7, 3, 'PriceList', format1)
            # if final_value['pricelist_id']:
            #     worksheet.write_merge(
            #         7, 7, 4, 5, final_value['pricelist_id'], format3)
            # worksheet.write(9, 0, 'Invoice Address', format1)
            # if final_value['partner_invoice_id']:
            #     worksheet.write(
            #         9, 1, final_value['partner_invoice_id'], format3)
            # worksheet.write(10, 0, 'Delivery Address', format1)
            # if final_value['partner_invoice_id']:
            #     worksheet.write(
            #         10, 1, final_value['partner_invoice_id'], format3)

            worksheet.write(8, 3, "Buyer", format1)
            if final_value['user_id']:
                worksheet.write_merge(
                    8, 8, 4, 5, final_value['user_id'], format3)
            worksheet.write(9, 3, "Source Document", format1)
            if final_value['origin']:
                worksheet.write_merge(
                    9, 9, 4, 5, final_value['origin'], format3)
            worksheet.write(10, 3, "Currency", format1)
            if final_value['currency_id']:
                worksheet.write_merge(
                    10, 10, 4, 5, sale_order.currency_id.name, format3)

            worksheet.write(13, 0, "Product", bold)
            worksheet.write(13, 1, "Description", bold)
            worksheet.write(13, 2, "Packaging", bold)
            worksheet.write(13, 3, "Packaging Qty", bold)
            worksheet.write(13, 4, "No of Packages", bold)

            worksheet.write(13, 5, "Total Qty", bold)
            worksheet.write(13, 6, "Product Uom", bold)
            worksheet.write(13, 7, "Unit Price", bold)
            worksheet.write(13, 8, "Carton Price", bold)

            # worksheet.write(13, 9, "Disc. (%)", bold)
            worksheet.write(13, 9, "Taxes", bold)
            worksheet.write(13, 10, "Subtotal", bold)

            row = 14

            for rec in order_lines:
                if rec.get('product_id'):
                    worksheet.write(row, 0, rec.get('product_id'), format3)
                if rec.get('description'):
                    worksheet.write(row, 1, rec.get('description'), format3)
                
                if rec.get('product_packaging_id'):
                    worksheet.write(row, 2, rec.get('product_packaging_id'), format3)

                if rec.get('test'):
                    worksheet.write(row, 3, rec.get('test'), format3)


                if rec.get('product_packaging_qty'):
                    worksheet.write(row, 4, rec.get('product_packaging_qty'), format3)

                if rec.get('product_uom_qty'):
                    worksheet.write(row, 5, rec.get(
                        'product_uom_qty'), format4)
                if rec.get('product_uom'):
                    worksheet.write(row, 6, rec.get('product_uom'), format4)
                if rec.get('price_unit'):
                    worksheet.write(row, 7, rec.get('price_unit'), format4)
                if rec.get('carton_price'):
                    worksheet.write(row, 8, rec.get('carton_price'), format4)

                # if rec.get('discount'):
                #     worksheet.write(row, 9, rec.get('discount'), format4)

                if rec.get('taxes_id'):
                    worksheet.write(row, 9, ",".join(
                        rec.get('taxes_id')), format4)
                    
                if rec.get('price_subtotal'):
                    worksheet.write(row, 10, rec.get('price_subtotal'), format4)
                    
                
                # else:
                #     worksheet.write(row, 10, '', format4)
                # if final_value['currency_id'].position == "before":
                #     worksheet.write(row, 10, rec.get('price_subtotal'), format4)
                # else:
                #     worksheet.write(row, 10, rec.get('price_subtotal'), format4)
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
            if final_value['notes']:
                worksheet.write_merge(
                    row, row+1, 0, 5, final_value['notes'], format3)

        filename = ('Purchase Order Xls Report' + '.xls')
        fp = BytesIO()
        workbook.save(fp)

        export_id = self.env['purchase.extended'].sudo().create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename,
        })

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=purchase.extended&field=excel_file&download=true&id=%s&filename=%s' % (export_id.id, export_id.file_name),
            'target': 'new',
        }
