# -*- coding: utf-8 -*-
"""
Attendance Regularization Dashboard Model
Provides analytics and dashboard functionality
"""

from odoo import api, fields, models
from datetime import datetime, timedelta


class AttendanceRegularizationDashboard(models.Model):
    """Dashboard model for attendance_regularization analytics"""
    _name = 'attendance_regularization.dashboard'
    _description = 'Attendance Regularization Dashboard'

    name = fields.Char(string='Dashboard Name', default='Attendance Regularization Analytics')
    total_records = fields.Integer(string='Total Records', compute='_compute_totals')
    records_today = fields.Integer(string='Records Today', compute='_compute_totals')
    records_this_month = fields.Integer(string='Records This Month', compute='_compute_totals')
    active_records = fields.Integer(string='Active Records', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute dashboard statistics"""
        for record in self:
            # Get actual statistics from attendance.regular model
            attendance_model = self.env['attendance.regular']
            today = datetime.now().date()
            month_start = today.replace(day=1)

            record.total_records = attendance_model.search_count([])
            record.records_today = attendance_model.search_count([
                ('create_date', '>=', today),
                ('create_date', '<', today + timedelta(days=1))
            ])
            record.records_this_month = attendance_model.search_count([
                ('create_date', '>=', month_start)
            ])
            record.active_records = attendance_model.search_count([
                ('state_select', '!=', 'cancel')
            ])

    def action_view_records(self):
        """Action to view all attendance regularization records"""
        return {
            'name': 'Attendance Regularization Records',
            'type': 'ir.actions.act_window',
            'res_model': 'attendance.regular',
            'view_mode': 'list,form',
            'target': 'current',
        }

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({})

        return {
            'totals': {
                'total_records': dashboard.total_records,
                'records_today': dashboard.records_today,
                'records_this_month': dashboard.records_this_month,
                'active_records': dashboard.active_records,
            },
        }
