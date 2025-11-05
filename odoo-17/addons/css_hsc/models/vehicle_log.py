# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError   # pyright: ignore[reportMissingImports]


class VehicleLog(models.Model):
    _name = 'vehicle.log'
    _description = 'vehicle Log'

    name = fields.Char(string="Employee Name")
    driver_name = fields.Char('Driver Name')
    mobile = fields.Char('Mobile no')
    attchment_ids = fields.Many2many('ir.attachment', string='Attchments')
    
    remarks = fields.Text(string='Remarks')

    log_type = fields.Selection([
        ('vehicle', 'Vehicles'),
        ('walkin', 'Walk-In'),
        ('others', 'Others'),
        ('shipment', 'Shipment'),
    ], string='Log Type',required=True)
    vehicle_number_id = fields.Many2one('vehicle.number', string='Vehicle Number')
    entry_log_category_id = fields.Many2one('entry.log.category', string='Category')
    category_search = fields.Binary('Category Search', compute='_compute_category_search')

    @api.depends('log_type')
    def _compute_category_search(self):
        VALUE_DICT={'vehicle':[1,2],'walkin':[1,3]}
        for page in  self:
            value=VALUE_DICT.get(page.log_type,[1])
            page.category_search = [('group_idx','in',value)]
           
   
    @api.onchange('vehicle_number_id')
    def _onchange_driver(self):
        self.driver_name = self.vehicle_number_id.driver_name
        self.mobile = self.vehicle_number_id.mobile
        

    

    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company, required=True, readonly=True)
    entry_type = fields.Selection([
        ('vehicle', 'vehicle'),
        ('walkin', 'walk In'),
    ], string='Entry', default='vehicle')
    purpose = fields.Char('Purpose')

    accompanied_count= fields.Integer('No of Accompanied')
   
    # document_name = fields.Char('Document Name')
    # document_given_by = fields.Char('Document Given By')
    # document_given_to = fields.Char('Document Given To')
    # collected_time = fields.Datetime('Collected Time')
    # delivered_time = fields.Datetime('Delivered Time')
    # courier_type = fields.Selection([
    #     ('inbound', 'Inbound'),
    #     ('outbound', 'Outbound'),
    # ], string='Courier Type')
    # courier_no = fields.Char('Courier Number')
    # courirer_from = fields.Char('Courirer From')
    # courier_to = fields.Char('Courier To')
    # courier_company = fields.Char('Courier Company')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'Check In'),
        ('checkout', 'Check Out'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    def validate_checkin(self):
        
        if self.env['vehicle.log'].search([('vehicle_number_id','=', self.vehicle_number_id.id),('state','=','checkin')]):
            raise UserError('Vehicle check in alredy exists!!!')
        
        

    def action_checkin(self):
        self.validate_checkin()
        self.state = 'checkin'
        self.time_in = fields.Datetime.now()
        
        

    def action_checkout(self):
        
        self.state = 'checkout'
        self.time_out = fields.Datetime.now()
        
        

    def action_cancel(self):
        if not self.remarks:
            raise UserError("Please Enter Remarks Before Checkout")
        self.state = 'cancelled'

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
