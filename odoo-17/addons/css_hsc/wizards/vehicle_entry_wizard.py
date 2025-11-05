# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError   # pyright: ignore[reportMissingImports]


class VehicleEntryWizard(models.TransientModel):
    _name = 'vehicle.entry.wizard'
    _description = 'Vehicle Entry Wizard'

    vehicle_number_id = fields.Many2one('vehicle.number', string='Vehicle Number', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    time_in = fields.Datetime('Time In')
    time_out = fields.Datetime('Time Out')
    time_out_km = fields.Integer('Time Out Km')
    time_in_km = fields.Integer('Time In Km')

    def submit_vehicle_entry(self):

        vehicle_type = self.vehicle_number_id.vehicle_type
        if vehicle_type == 'external':
            vehicle_type='visitors'
     

        category_id = self.env['entry.log.category'].search([('code','=', vehicle_type)],limit = 1)
        
        vals = {
            'entry_log_category_id':category_id.id,
            'vehicle_number_id':self.vehicle_number_id.id,
            'driver_name':self.vehicle_number_id.driver_name,
            'mobile':self.vehicle_number_id.mobile,
            'purpose':False,
            'accompanied_count':0,
            'remarks':False,
            'log_type':'vehicle',
            'time_out_km':self.time_out_km,
            'time_in_km':self.time_in_km,
            }
       
        log_id = self.env['vehicle.log'].create(vals)
        log_id.action_checkin()
       
        

       
        
        
