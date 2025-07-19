# -*- coding: utf-8 -*-
"""
Stock Alert Notification Model
Handles email notifications for low stock alerts
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockAlertNotification(models.Model):
    """Model to handle stock alert notifications"""
    _name = 'stock.alert.notification'
    _description = 'Stock Alert Notification'
    _order = 'create_date desc'

    name = fields.Char(string='Notification Reference', required=True, default='New')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    current_stock = fields.Float(string='Current Stock', required=True)
    minimum_stock = fields.Float(string='Minimum Stock Level', required=True)
    notification_date = fields.Datetime(string='Notification Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
    ], string='Status', default='draft')
    recipient_ids = fields.Many2many('res.users', string='Recipients')
    email_sent = fields.Boolean(string='Email Sent', default=False)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        """Override create to generate sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.alert.notification') or 'New'
        return super().create(vals)

    def action_send_notification(self):
        """Send email notification to recipients"""
        for record in self:
            if not record.recipient_ids:
                # Get default recipients (inventory managers)
                recipients = self.env['res.users'].search([
                    ('groups_id', 'in', self.env.ref('stock.group_stock_manager').id)
                ])
                record.recipient_ids = [(6, 0, recipients.ids)]
            
            if record.recipient_ids:
                # Send email using mail template
                template = self.env.ref('low_stocks_product_alert.email_template_stock_alert', 
                                      raise_if_not_found=False)
                if template:
                    for recipient in record.recipient_ids:
                        template.with_context(
                            recipient_user=recipient,
                            notification_record=record
                        ).send_mail(record.id, force_send=True)
                    
                    record.write({
                        'state': 'sent',
                        'email_sent': True
                    })
                    _logger.info(f"Stock alert notification sent for product {record.product_id.name}")
                else:
                    raise UserError(_("Email template for stock alerts not found."))
            else:
                raise UserError(_("No recipients found for stock alert notification."))

    def action_acknowledge(self):
        """Mark notification as acknowledged"""
        self.write({'state': 'acknowledged'})

    @api.model
    def create_stock_alert(self, product_id, current_stock, minimum_stock):
        """Create a new stock alert notification"""
        # Check if alert already exists for this product today
        today = fields.Date.today()
        existing_alert = self.search([
            ('product_id', '=', product_id),
            ('create_date', '>=', today),
            ('create_date', '<', today + fields.timedelta(days=1))
        ], limit=1)
        
        if not existing_alert:
            alert = self.create({
                'product_id': product_id,
                'current_stock': current_stock,
                'minimum_stock': minimum_stock,
            })
            
            # Auto-send if configured
            auto_send = self.env['ir.config_parameter'].sudo().get_param(
                'low_stocks_product_alert.auto_send_notifications', default=False
            )
            if auto_send:
                alert.action_send_notification()
            
            return alert
        
        return existing_alert

    @api.model
    def check_and_create_alerts(self):
        """Scheduled method to check stock levels and create alerts"""
        stock_alert_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'low_stocks_product_alert.is_low_stock_alert'
        )
        
        if stock_alert_enabled:
            min_stock_level = int(self.env['ir.config_parameter'].sudo().get_param(
                'low_stocks_product_alert.min_low_stock_alert', default=5
            ))
            
            # Get products with low stock
            products = self.env['product.product'].search([
                ('type', '=', 'product'),
                ('qty_available', '<=', min_stock_level),
                ('active', '=', True)
            ])
            
            alerts_created = 0
            for product in products:
                alert = self.create_stock_alert(
                    product.id, 
                    product.qty_available, 
                    min_stock_level
                )
                if alert:
                    alerts_created += 1
            
            _logger.info(f"Created {alerts_created} stock alert notifications")
            return alerts_created
        
        return 0
