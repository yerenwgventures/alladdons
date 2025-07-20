# -*- coding: utf-8 -*-
"""
User Audit Dashboard Model
Provides analytics and dashboard functionality for user audit logs
"""

from odoo import api, fields, models
from datetime import datetime, timedelta


class AuditDashboard(models.Model):
    """Dashboard model for user audit analytics"""
    _name = 'audit.dashboard'
    _description = 'User Audit Dashboard'
    # _auto = False  # Fixed: Create table

    name = fields.Char(string='Dashboard Name', default='Audit Analytics')
    total_audits = fields.Integer(string='Total Audit Logs', compute='_compute_totals')
    audits_today = fields.Integer(string='Audits Today', compute='_compute_totals')
    audits_this_week = fields.Integer(string='Audits This Week', compute='_compute_totals')
    audits_this_month = fields.Integer(string='Audits This Month', compute='_compute_totals')
    most_active_user = fields.Char(string='Most Active User', compute='_compute_totals')
    most_accessed_model = fields.Char(string='Most Accessed Model', compute='_compute_totals')
    login_count_today = fields.Integer(string='Logins Today', compute='_compute_totals')
    failed_login_attempts = fields.Integer(string='Failed Logins Today', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute dashboard statistics"""
        for record in self:
            # Get all audit logs
            audits = self.env['user.audit'].search([])
            
            record.total_audits = len(audits)
            
            # Today's audits
            today = fields.Date.today()
            today_audits = audits.filtered(
                lambda x: x.create_date and x.create_date.date() == today
            )
            record.audits_today = len(today_audits)
            
            # This week's audits
            week_start = today - timedelta(days=today.weekday())
            week_audits = audits.filtered(
                lambda x: x.create_date and x.create_date.date() >= week_start
            )
            record.audits_this_week = len(week_audits)
            
            # This month's audits
            month_start = today.replace(day=1)
            month_audits = audits.filtered(
                lambda x: x.create_date and x.create_date.date() >= month_start
            )
            record.audits_this_month = len(month_audits)
            
            # Most active user
            if audits:
                user_activity = {}
                for audit in audits:
                    user = audit.user_id.name if audit.user_id else 'Unknown'
                    user_activity[user] = user_activity.get(user, 0) + 1
                
                if user_activity:
                    record.most_active_user = max(user_activity, key=user_activity.get)
                else:
                    record.most_active_user = 'No activity'
            else:
                record.most_active_user = 'No audits yet'
            
            # Most accessed model
            if audits:
                model_activity = {}
                for audit in audits:
                    model = audit.model_name or 'Unknown'
                    model_activity[model] = model_activity.get(model, 0) + 1
                
                if model_activity:
                    record.most_accessed_model = max(model_activity, key=model_activity.get)
                else:
                    record.most_accessed_model = 'No model data'
            else:
                record.most_accessed_model = 'No audits yet'
            
            # Login statistics (simplified)
            record.login_count_today = len(today_audits.filtered(lambda x: 'login' in (x.action or '').lower()))
            record.failed_login_attempts = len(today_audits.filtered(lambda x: 'failed' in (x.action or '').lower()))

    def get_audit_trends(self):
        """Return audit trend data for charts"""
        audits = self.env['user.audit'].search([])
        
        # Last 7 days trend
        trend_data = {}
        for i in range(7):
            date = fields.Date.today() - timedelta(days=i)
            day_audits = audits.filtered(
                lambda x: x.create_date and x.create_date.date() == date
            )
            trend_data[date.strftime('%Y-%m-%d')] = len(day_audits)
        
        return trend_data

    def get_user_activity_breakdown(self):
        """Return user activity breakdown"""
        audits = self.env['user.audit'].search([])
        user_data = {}
        
        for audit in audits:
            user = audit.user_id.name if audit.user_id else 'Unknown'
            user_data[user] = user_data.get(user, 0) + 1
        
        return user_data

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({})
        
        return {
            'totals': {
                'total_audits': dashboard.total_audits,
                'audits_today': dashboard.audits_today,
                'audits_this_week': dashboard.audits_this_week,
                'audits_this_month': dashboard.audits_this_month,
                'most_active_user': dashboard.most_active_user,
                'most_accessed_model': dashboard.most_accessed_model,
                'login_count_today': dashboard.login_count_today,
                'failed_login_attempts': dashboard.failed_login_attempts,
            },
            'trends': dashboard.get_audit_trends(),
            'user_activity': dashboard.get_user_activity_breakdown(),
        }
    def action_view_records(self):
        """Action to view all records"""
        return {
            'name': 'Records',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'list,form',
            'target': 'current',
        }
