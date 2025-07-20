# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrPayslip(models.Model):
    """Stub model for hr.payslip"""
    _name = 'hr.payslip'
    _description = 'Payslip Stub'

    name = fields.Char(string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    payslip_run_id = fields.Many2one('hr.payslip.run', string='Payslip Run')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', default='draft')
    
class HrPayslipLine(models.Model):
    """Stub model for hr.payslip.line"""
    _name = 'hr.payslip.line'
    _description = 'Payslip Line Stub'
    
    name = fields.Char(string='Name', required=True)
    slip_id = fields.Many2one('hr.payslip', string='Pay Slip')
    amount = fields.Float(string='Amount')
    
class HrSalaryRule(models.Model):
    """Stub model for hr.salary.rule"""
    _name = 'hr.salary.rule'
    _description = 'Salary Rule Stub'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    
class HrPayrollStructure(models.Model):
    """Stub model for hr.payroll.structure"""
    _name = 'hr.payroll.structure'
    _description = 'Payroll Structure Stub'
    
    name = fields.Char(string='Name', required=True)
