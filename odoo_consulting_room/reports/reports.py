# -*- coding: utf-8 -*-

import io

from odoo import fields, api, models

from odoo.tools.misc import xlwt
from collections import defaultdict

class ReportTreatments(models.TransientModel):
    _name = 'odoo_consulting_room.treatments'

    def print_excel(self):
        self.ensure_one()
        url = '/web/binary/download_export_report_treatments?id={}&filename=reporte_de_tratamientos_mas_solicitados_por_los_pacientes.xls'.format(self.id)
        value = {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }
        return value

    def generate_xlsx_report(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')

        xlwt.add_palette_colour("custom_colour", 0x21)
        workbook.set_colour_RGB(0x21, 68, 114, 196)

        style0 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )
        style1 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index white;pattern: pattern solid, fore_colour custom_colour; align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )
        style1_1 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index white;pattern: pattern solid, fore_colour custom_colour; align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )

        s0_t = 0
        s0 = 1
        s1 = 2
        s2 = 3
        s3 = 4
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 10500
        worksheet.col(2).width = 10500
        worksheet.col(3).width = 10500
        worksheet.col(21).width = 10000
        worksheet.col(22).width = 15000
        worksheet.col(23).width = 10000
        worksheet.col(24).width = 15000
        worksheet.col(25).width = 10000
        worksheet.col(26).width = 10000
        worksheet.col(27).width = 10000

        worksheet.write_merge(s0_t, s0_t, 2, 15, u'Informe de tratamientos más solicitados por los pacientes', style1)
        worksheet.write(s2, 1, u'Tratamiento', style1_1)
        worksheet.write(s2, 2, u'Cantidad', style1_1)
        worksheet.write(s2, 3, u'Monto Facturado', style1_1)

        treatments = []
        for record in self.env['odoo_consulting_room.treatmentspatient'].search([]):
            treatments.append(record.type_treatments)

        D = defaultdict(list)
        for i, item in enumerate(treatments):
            D[item].append(i)
        D = {k: v for k, v in D.items() if len(v) > 2}
        tream = []
        qty = []
        for k, v in D.items():
            tream.append(k)
            qty.append(v)

        mount_total = 0
        for record_patient in self.env['odoo_consulting_room.patientrecord'].search([]):
            for trems in record_patient.trataments_ids:
                if trems.type_treatments == tream[0]:
                    mount_total = mount_total + trems.mount

        worksheet.write(s3, 1, str(tream[0]), style0)
        worksheet.write(s3, 2, len(qty[0]), style0)
        worksheet.write(s3, 3, mount_total, style0)
        s3 += 1

        file_data = io.BytesIO()
        workbook.save(file_data)
        file_data.seek(0)
        data = file_data.read()
        file_data.close()
        return data


class ReportAttended(models.TransientModel):
    _name = 'odoo_consulting_room.attended'

    def print_excel(self):
        self.ensure_one()
        url = '/web/binary/download_export_report_attended?id={}&filename=Reporte_de_pacientes_que_asistieron_a_menos_consultas.xls'.format(self.id)
        value = {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }
        return value

    def generate_xlsx_report(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')

        xlwt.add_palette_colour("custom_colour", 0x21)
        workbook.set_colour_RGB(0x21, 68, 114, 196)

        style0 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )
        style1 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index white;pattern: pattern solid, fore_colour custom_colour; align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )
        style1_1 = xlwt.easyxf(
            'font: height 200, name Calibri, colour_index white;pattern: pattern solid, fore_colour custom_colour; align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
        )

        s0_t = 0
        s0 = 1
        s1 = 2
        s2 = 3
        s3 = 4
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 10500
        worksheet.col(2).width = 10500
        worksheet.col(3).width = 10500
        worksheet.col(21).width = 10000
        worksheet.col(22).width = 15000
        worksheet.col(23).width = 10000
        worksheet.col(24).width = 15000
        worksheet.col(25).width = 10000
        worksheet.col(26).width = 10000
        worksheet.col(27).width = 10000

        worksheet.write_merge(s0_t, s0_t, 2, 15, u'Reporte de pacientes que asistieron a menos consultas', style1)
        worksheet.write(s2, 1, u'Pacientes', style1_1)

        qty_attended = 0
        patient = []
        for record in self.env['odoo_consulting_room.patientrecord'].search([]):
            patient.append(record.id)
            qty_attended = qty_attended + record.qty_consultations_attended
        prom_attended = qty_attended / len(patient)
        for record in self.env['odoo_consulting_room.patientrecord'].search([]):
            if record.qty_consultations_attended < int(prom_attended):
                worksheet.write(s3, 1, record.name, style0)
                s3 += 1

        file_data = io.BytesIO()
        workbook.save(file_data)
        file_data.seek(0)
        data = file_data.read()
        file_data.close()
        return data