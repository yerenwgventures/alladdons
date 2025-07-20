# -*- coding: utf-8 -*-
"""
Print Button Analytics Model
Provides analytics for print button usage across the system
"""

from odoo import api, fields, models
from datetime import datetime, timedelta


class PrintButtonAnalytics(models.Model):
    """Analytics model for print button usage"""
    _name = 'print.button.analytics'
    _description = 'Print Button Usage Analytics'
    # _auto = False  # Fixed: Create table

    name = fields.Char(string='Analytics Name', default='Print Button Analytics')
    total_users = fields.Integer(string='Total Users', compute='_compute_totals')
    users_with_print_access = fields.Integer(string='Users with Print Access', compute='_compute_totals')
    users_without_print_access = fields.Integer(string='Users without Print Access', compute='_compute_totals')
    print_access_percentage = fields.Float(string='Print Access Percentage', compute='_compute_totals')
    most_restricted_model = fields.Char(string='Most Restricted Model', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute analytics statistics"""
        for record in self:
            # Get all users
            all_users = self.env['res.users'].search([('active', '=', True)])
            record.total_users = len(all_users)
            
            # Count users with print restrictions
            users_with_restrictions = 0
            users_without_restrictions = 0
            
            for user in all_users:
                has_restrictions = (
                    not user.print_account_move or
                    not user.print_sale_order or
                    not user.print_purchase_order or
                    not user.print_stock_picking
                )
                
                if has_restrictions:
                    users_with_restrictions += 1
                else:
                    users_without_restrictions += 1
            
            record.users_with_print_access = users_without_restrictions
            record.users_without_print_access = users_with_restrictions
            
            # Calculate percentage
            if record.total_users > 0:
                record.print_access_percentage = (users_without_restrictions / record.total_users) * 100
            else:
                record.print_access_percentage = 0.0
            
            # Find most restricted model (simplified)
            restriction_counts = {
                'Account Move': len(all_users.filtered(lambda u: not u.print_account_move)),
                'Sale Order': len(all_users.filtered(lambda u: not u.print_sale_order)),
                'Purchase Order': len(all_users.filtered(lambda u: not u.print_purchase_order)),
                'Stock Picking': len(all_users.filtered(lambda u: not u.print_stock_picking)),
            }
            
            if restriction_counts:
                record.most_restricted_model = max(restriction_counts, key=restriction_counts.get)
            else:
                record.most_restricted_model = 'None'

    def get_restriction_breakdown(self):
        """Return breakdown of restrictions by model"""
        all_users = self.env['res.users'].search([('active', '=', True)])
        
        return {
            'account_move': len(all_users.filtered(lambda u: not u.print_account_move)),
            'sale_order': len(all_users.filtered(lambda u: not u.print_sale_order)),
            'purchase_order': len(all_users.filtered(lambda u: not u.print_purchase_order)),
            'stock_picking': len(all_users.filtered(lambda u: not u.print_stock_picking)),
        }

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({})
        
        return {
            'totals': {
                'total_users': dashboard.total_users,
                'users_with_print_access': dashboard.users_with_print_access,
                'users_without_print_access': dashboard.users_without_print_access,
                'print_access_percentage': dashboard.print_access_percentage,
                'most_restricted_model': dashboard.most_restricted_model,
            },
            'restrictions': dashboard.get_restriction_breakdown(),
        }
