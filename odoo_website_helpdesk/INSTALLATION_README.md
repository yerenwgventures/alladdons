# Website Helpdesk Management

## Overview
The website allows for the creation of tickets, which can 
    then be controlled from the backend.

## Installation

### Prerequisites
**Required Odoo Modules:**
- website
- project

**Custom Dependencies:**
- sale_project (ensure this module is available)
- hr_timesheet (ensure this module is available)
- contacts (ensure this module is available)

### Installation Steps
1. Ensure all prerequisites are installed
2. Copy the `odoo_website_helpdesk` folder to your Odoo addons directory
3. Restart Odoo server
4. Update apps list: Settings → Apps → Update Apps List
5. Search for "Website Helpdesk Management"
6. Click Install

## Compatibility

### Odoo Version
- **Supported:** Odoo 18.0
- **Version:** 18.0.1.0.2

### Potential Conflicts
⚠️ Custom dependency: sale_project
⚠️ Custom dependency: hr_timesheet
⚠️ Custom dependency: contacts

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
