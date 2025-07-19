# -*- coding: utf-8 -*-
"""
Database Performance Optimizations for pos_kitchen_screen_odoo
Adds indexes to frequently queried fields
"""

from odoo import api, fields, models, tools


class PosKitchenScreenOdooPerformanceOptimization(models.AbstractModel):
    """Performance optimization model for pos_kitchen_screen_odoo"""
    _name = 'pos_kitchen_screen_odoo.performance.optimization'
    _description = 'Performance Optimization for Pos Kitchen Screen Odoo'

    @api.model
    def init_performance_indexes(self):
        """Initialize performance indexes"""
        # Add indexes for frequently queried fields
        indexes_to_create = {'pos_order': ['state', 'date_order'], 'pos_order_line': ['order_id', 'product_id']}
        
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
