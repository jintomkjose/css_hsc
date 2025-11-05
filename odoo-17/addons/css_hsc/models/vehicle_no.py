# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError   # pyright: ignore[reportMissingImports]


class VehicleNumber(models.Model):
    _name = 'vehicle.number'
    _description = 'Vehicle Number'

    name = fields.Char(string="Vehicle Number", required=True)
    vehicle_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
        ('staff', 'Staff'),
    ], string='Vehicle Type', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    partner_id = fields.Many2one('res.partner', string='Partner')
    driver_name = fields.Char('Driver Name',required=True)
    mobile = fields.Char('Driver Mobile')
    id_proof = fields.Char('ID Proof')
    


    @api.onchange('employee_id','partner_id','vehicle_type')
    def _onchange_driver(self):
        partner_id=self.partner_id
       
        if self.vehicle_type != 'external':
            partner_id=self.employee_id.work_contact_id
        
        self.driver_name=partner_id.name
        self.mobile=partner_id.mobile 

            
        



class EntryLogCategory(models.Model):
    _name = 'entry.log.category'
    _description = 'Category for Entry Log'

    name = fields.Char(string="Category", required=True)
    code = fields.Char(string="Code", required=True)
    group_idx = fields.Integer('Group', default=1)

   


