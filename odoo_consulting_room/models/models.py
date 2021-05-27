# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PatientRecord(models.Model):
    _name = 'odoo_consulting_room.patientrecord'
    _description = 'Registro de pacientes'
    _red_name = 'name'

    dni = fields.Char(
        string='DNI',
        required=True,
        size=8,
    )
    name = fields.Char(
        string='Nombre',
        required=True
    )
    last_name = fields.Char(
        string='Apellidos',
        required=True
    )
    qty_consultations_attended = fields.Integer(
        string='Número de consultas atendidas al centro',
    )
    qty_treatments = fields.Integer(
        string='Número de tratamientos realizados',
        compute='_compute_qty_treatments',
        store=True
    )
    trataments_ids = fields.One2many(
        comodel_name='odoo_consulting_room.treatmentspatient',
        inverse_name='patiente_record_id',
        string='Tratamientos realizados'
    )

    @api.constrains('dni')
    def _check_dni(self):
        if self.dni and not self.dni.isdigit():
            raise ValidationError('Solo se deben ingresar números en el campo DNI')

    @api.depends('trataments_ids')
    def _compute_qty_treatments(self):
        for record in self:
            if record.trataments_ids:
                record.qty_treatments = len(record.trataments_ids)


class TreatmentsPatient(models.Model):
    _name = 'odoo_consulting_room.treatmentspatient'
    _description = 'Tratamientos de pacientes'
    _red_name = 'type_treatments'

    type_treatments = fields.Char(
        string='Tipos de tratamientos realizados',
        required=True
    )
    mount = fields.Float(
        string='Monto a facturar'
    )
    patiente_record_id = fields.Many2one(
        comodel_name='odoo_consulting_room.patientrecord',
        string='Registro de paciente'
    )
