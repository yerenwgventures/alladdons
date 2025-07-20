# Alternative Products in Pos

## Overview
We can select alternative product , when a product have 
     zero available quantity in pos.

## Installation

### Prerequisites
**Required Odoo Modules:**
- website

**Custom Dependencies:**
- stub_point_of_sale (ensure this module is available)
- pos_sale (ensure this module is available)
- stub_website_sale (ensure this module is available)

### Installation Steps
1. Ensure all prerequisites are installed
2. Copy the `pos_alternative_products` folder to your Odoo addons directory
3. Restart Odoo server
4. Update apps list: Settings → Apps → Update Apps List
5. Search for "Alternative Products in Pos"
6. Click Install

## Compatibility

### Odoo Version
- **Supported:** Odoo 18.0
- **Version:** 18.0.1.0.0

### Potential Conflicts
⚠️ Requires custom stub: stub_point_of_sale
⚠️ Custom dependency: pos_sale
⚠️ Requires custom stub: stub_website_sale

**Recommendation:** Test in staging environment before production deployment.

## Production Status
⚠️ **REQUIRES REVIEW** - Please address issues before production use

## Module Information
- **Category:** Website
- **Author:** CBMS TECHNOLOGIES LTD
- **Maintainer:** CBMS TECHNOLOGIES LTD

## Support
For technical support or installation issues, please contact your system administrator or CBMS support team.

---
*This README was automatically generated for production deployment.*
