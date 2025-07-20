# -*- coding: utf-8 -*-
"""
UOM Analytics Model
Provides analytics for Unit of Measure usage and product listings
"""

from odoo import api, fields, models
from datetime import datetime, timedelta


class UomAnalytics(models.Model):
    """Analytics model for UOM usage"""
    _name = 'uom.analytics'
    _description = 'UOM Usage Analytics'

    name = fields.Char(string='Analytics Name', default='UOM Analytics')
    total_uoms = fields.Integer(string='Total UOMs', compute='_compute_totals')
    active_uoms = fields.Integer(string='Active UOMs', compute='_compute_totals')
    products_with_uom = fields.Integer(string='Products with UOM', compute='_compute_totals')
    most_used_uom = fields.Char(string='Most Used UOM', compute='_compute_totals')
    uom_categories_count = fields.Integer(string='UOM Categories', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute analytics statistics"""
        for record in self:
            # Get all UOMs
            all_uoms = self.env['uom.uom'].search([])
            active_uoms = all_uoms.filtered(lambda u: u.active)
            
            record.total_uoms = len(all_uoms)
            record.active_uoms = len(active_uoms)
            
            # Get products with UOM
            products = self.env['product.template'].search([])
            products_with_uom = products.filtered(lambda p: p.uom_id)
            record.products_with_uom = len(products_with_uom)
            
            # Find most used UOM
            if products_with_uom:
                uom_usage = {}
                for product in products_with_uom:
                    uom_name = product.uom_id.name
                    uom_usage[uom_name] = uom_usage.get(uom_name, 0) + 1
                
                if uom_usage:
                    record.most_used_uom = max(uom_usage, key=uom_usage.get)
                else:
                    record.most_used_uom = 'None'
            else:
                record.most_used_uom = 'No products found'
            
            # Count UOM categories
            categories = self.env['uom.category'].search([])
            record.uom_categories_count = len(categories)

    def get_uom_usage_breakdown(self):
        """Return breakdown of UOM usage by category"""
        products = self.env['product.template'].search([])
        category_usage = {}
        
        for product in products:
            if product.uom_id and product.uom_id.category_id:
                category_name = product.uom_id.category_id.name
                category_usage[category_name] = category_usage.get(category_name, 0) + 1
        
        return category_usage

    def get_top_uoms(self, limit=10):
        """Return top used UOMs"""
        products = self.env['product.template'].search([])
        uom_usage = {}
        
        for product in products:
            if product.uom_id:
                uom_name = product.uom_id.name
                uom_usage[uom_name] = uom_usage.get(uom_name, 0) + 1
        
        # Sort by usage and return top N
        sorted_uoms = sorted(uom_usage.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_uoms[:limit])

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({})
        
        return {
            'totals': {
                'total_uoms': dashboard.total_uoms,
                'active_uoms': dashboard.active_uoms,
                'products_with_uom': dashboard.products_with_uom,
                'most_used_uom': dashboard.most_used_uom,
                'uom_categories_count': dashboard.uom_categories_count,
            },
            'category_usage': dashboard.get_uom_usage_breakdown(),
            'top_uoms': dashboard.get_top_uoms(),
        }
