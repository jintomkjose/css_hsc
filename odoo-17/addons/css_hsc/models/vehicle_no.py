# -*- coding: utf-8 -*-

import datetime as dt
from odoo import models, fields, api
from odoo.exceptions import UserError   # pyright: ignore[reportMissingImports]

VTYPE= {
            'internal' :'checkout',
        }

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
    last_km_reading = fields.Integer('Total KM',readonly=True)
    meter_reading  = fields.Char('Meter Reading ')
    

    def validate_checkin(self):
        state =VTYPE.get(self.vehicle_type, 'checkin')
        if self.env['vehicle.log'].search([('vehicle_number_id', '=', self.id), ('state', '=', state)]):
            raise UserError('Vehicle check in alredy exists!!!')
    
    def _check_reading(self, current_reading):
        
        if self.last_km_reading > current_reading:
            raise UserError(f'Cannot update vehicle meter reading. New reading should be higher than current odomerter reading. {self.last_km_reading}')
        self.last_km_reading = current_reading



    def _create_vehicle_entry(self, category_id,  last_km_reading=0, time_in=False):
        self.validate_checkin()
        self._check_reading(last_km_reading)
        

        vals = {
            'vehicle_number_id' : self.id,
            'partner_id' : self.partner_id.id,
            'driver_name':self.driver_name,
            'mobile':self.mobile,
            'log_type':'vehicle',
            'time_in' : time_in or dt.datetime.now(),
            'time_out_km' : self.last_km_reading,
            'entry_log_category_id' : category_id.id,
            'state' : VTYPE.get(self.vehicle_type, 'checkin')

        }

        log_id = self.env['vehicle.log'].create(vals)
        log_id._action_log_entry()
     

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

   


