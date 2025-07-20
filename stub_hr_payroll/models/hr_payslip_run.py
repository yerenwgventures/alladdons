# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrPayslipRun(models.Model):
    """Stub model for hr.payslip.run"""
    _name = 'hr.payslip.run'
    _description = 'Payslip Run Stub'
    
    name = fields.Char(string='Name', required=True)
    date_start = fields.Date(string='Date From')
    date_end = fields.Date(string='Date To')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('close', 'Close'),
    ], string='Status', default='draft')
    slip_ids = fields.One2many('hr.payslip', 'payslip_run_id', string='Payslips')
