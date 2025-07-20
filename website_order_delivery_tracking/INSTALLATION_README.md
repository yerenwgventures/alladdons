# Website Order Delivery Tracking

## Overview
Track order delivery status, and delivery partners can update 
    the status.

## Installation

### Prerequisites
**Required Odoo Modules:**
- website
- stock

**Custom Dependencies:**
- stub_sale_stock (ensure this module is available)
- sale_management (ensure this module is available)
- stock_delivery (ensure this module is available)

### Installation Steps
1. Ensure all prerequisites are installed
2. Copy the `website_order_delivery_tracking` folder to your Odoo addons directory
3. Restart Odoo server
4. Update apps list: Settings → Apps → Update Apps List
5. Search for "Website Order Delivery Tracking"
6. Click Install

## Compatibility

### Odoo Version
- **Supported:** Odoo 18.0
- **Version:** 18.0.1.0.0

### Potential Conflicts
⚠️ Requires custom stub: stub_sale_stock
⚠️ Custom dependency: sale_management
⚠️ Custom dependency: stock_delivery

**Recommendation:** Test in staging environment before production deployment.

## Production Status
⚠️ **REQUIRES REVIEW** - Please address issues before production use

## Module Information
- **Category:** Website
- **Author:** Cybrosys Techno Solutions
- **Maintainer:** CBMS TECHNOLOGIES LTD

## Support
For technical support or installation issues, please contact your system administrator or CBMS support team.

---
*This README was automatically generated for production deployment.*
