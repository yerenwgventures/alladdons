# -*- coding: utf-8 -*-
"""
Employee Ideas Dashboard Model
Provides analytics and dashboard functionality for employee ideas
"""

from odoo import api, fields, models
from odoo.tools import float_utils


class IdeaDashboard(models.Model):
    """Dashboard model for employee ideas analytics"""
    _name = 'idea.dashboard'
    _description = 'Employee Ideas Dashboard'
    _auto = False

    name = fields.Char(string='Dashboard Name', default='Ideas Analytics')
    total_ideas = fields.Integer(string='Total Ideas', compute='_compute_totals')
    pending_ideas = fields.Integer(string='Pending Ideas', compute='_compute_totals')
    approved_ideas = fields.Integer(string='Approved Ideas', compute='_compute_totals')
    rejected_ideas = fields.Integer(string='Rejected Ideas', compute='_compute_totals')
    ideas_this_month = fields.Integer(string='Ideas This Month', compute='_compute_totals')
    top_contributor = fields.Char(string='Top Contributor', compute='_compute_totals')
    avg_votes_per_idea = fields.Float(string='Average Votes per Idea', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute dashboard statistics"""
        for record in self:
            # Get all ideas
            ideas = self.env['employee.idea'].search([])
            
            record.total_ideas = len(ideas)
            record.pending_ideas = len(ideas.filtered(lambda x: x.state == 'draft'))
            record.approved_ideas = len(ideas.filtered(lambda x: x.state == 'approved'))
            record.rejected_ideas = len(ideas.filtered(lambda x: x.state == 'rejected'))
            
            # Ideas this month
            from datetime import datetime, timedelta
            first_day_month = datetime.now().replace(day=1)
            record.ideas_this_month = len(ideas.filtered(
                lambda x: x.create_date and x.create_date >= first_day_month
            ))
            
            # Top contributor
            if ideas:
                contributors = {}
                for idea in ideas:
                    employee = idea.employee_id.name if idea.employee_id else 'Unknown'
                    contributors[employee] = contributors.get(employee, 0) + 1
                
                if contributors:
                    record.top_contributor = max(contributors, key=contributors.get)
                else:
                    record.top_contributor = 'No contributors'
            else:
                record.top_contributor = 'No ideas yet'
            
            # Average votes per idea
            if ideas:
                total_votes = sum(idea.vote_count for idea in ideas if idea.vote_count)
                record.avg_votes_per_idea = total_votes / len(ideas) if ideas else 0.0
            else:
                record.avg_votes_per_idea = 0.0

    def get_ideas_by_status(self):
        """Return ideas grouped by status for charts"""
        ideas = self.env['employee.idea'].search([])
        status_data = {
            'draft': len(ideas.filtered(lambda x: x.state == 'draft')),
            'approved': len(ideas.filtered(lambda x: x.state == 'approved')),
            'rejected': len(ideas.filtered(lambda x: x.state == 'rejected')),
        }
        return status_data

    def get_monthly_ideas_trend(self):
        """Return monthly trend data for ideas"""
        from datetime import datetime, timedelta
        import calendar
        
        ideas = self.env['employee.idea'].search([])
        monthly_data = {}
        
        for i in range(12):
            month_start = datetime.now().replace(day=1, month=datetime.now().month - i)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            
            month_ideas = ideas.filtered(
                lambda x: x.create_date and month_start <= x.create_date <= month_end
            )
            
            month_name = calendar.month_name[month_start.month]
            monthly_data[month_name] = len(month_ideas)
        
        return monthly_data

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({})
        
        return {
            'totals': {
                'total_ideas': dashboard.total_ideas,
                'pending_ideas': dashboard.pending_ideas,
                'approved_ideas': dashboard.approved_ideas,
                'rejected_ideas': dashboard.rejected_ideas,
                'ideas_this_month': dashboard.ideas_this_month,
                'top_contributor': dashboard.top_contributor,
                'avg_votes_per_idea': dashboard.avg_votes_per_idea,
            },
            'status_chart': dashboard.get_ideas_by_status(),
            'monthly_trend': dashboard.get_monthly_ideas_trend(),
        }
