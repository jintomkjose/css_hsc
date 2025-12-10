# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError   # pyright: ignore[reportMissingImports]


class walkinwizard(models.TransientModel):
    _name = 'walkin.entry.wizard'
    _description = 'Walkin Entry Wizard'

    walkin_type = fields.Selection([
        ('staff', 'staff'),
        ('visitor', 'visitor'),
        ('labor', 'labor'),
    ], string='Walkin Type')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
   
    
    def submit_vehicle_entry(self):
        self._action_entry()
        
    
    def submit_vehicle_exit(self):
        self._action_entry()

    



    def _action_entry(self):

        CAT_DICT = {
            'staff':'css_hsc.data_entry_category_staff',
            'internal':'css_hsc.data_entry_category_css_internal' 
        }

        entry_log_category_id = self.env.ref(CAT_DICT.get(self.vehicle_number_id.vehicle_type,'css_hsc.data_entry_category_visitors'))
        self.vehicle_number_id._create_vehicle_entry(entry_log_category_id, self.meter_reading)

    

    
        
        

       
        
        
