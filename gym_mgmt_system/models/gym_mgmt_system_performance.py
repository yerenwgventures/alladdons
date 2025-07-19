# -*- coding: utf-8 -*-
"""
Database Performance Optimizations for gym_mgmt_system
Adds indexes to frequently queried fields
"""

from odoo import api, fields, models, tools


class GymMgmtSystemPerformanceOptimization(models.AbstractModel):
    """Performance optimization model for gym_mgmt_system"""
    _name = 'gym_mgmt_system.performance.optimization'
    _description = 'Performance Optimization for Gym Mgmt System'

    @api.model
    def init_performance_indexes(self):
        """Initialize performance indexes"""
        # Add indexes for frequently queried fields
        indexes_to_create = {'gym_membership': ['reference', 'state', 'member_id'], 'gym_member': ['membership_id', 'active']}
        
        for table, fields_list in indexes_to_create.items():
            for field in fields_list:
                index_name = f"idx_{table}_{field}"
                
                # Check if index exists
                self.env.cr.execute("""
                    SELECT indexname FROM pg_indexes 
                    WHERE tablename = %s AND indexname = %s
                """, (table, index_name))
                
                if not self.env.cr.fetchone():
                    # Create index
                    try:
                        self.env.cr.execute(f"""
                            CREATE INDEX {index_name} ON {table} ({field})
                        """)
                        print(f"Created index {index_name} on {table}.{field}")
                    except Exception as e:
                        print(f"Failed to create index {index_name}: {e}")

    @api.model
    def optimize_queries(self):
        """Optimize common database queries"""
        # This method would contain optimized query patterns
        # specific to the module's most common operations
        pass
