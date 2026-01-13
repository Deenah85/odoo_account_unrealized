# -*- coding: utf-8 -*-

{
    'name': 'Unrealized Currency Gains/Losses (Community)',
    'version': '18.0.1.0.1',
    'author': 'Dina Sarhan',
    'category': 'Accounting/Reporting',
    'summary': 'Unrealized currency gains and losses report for Odoo 18 Community',
    'description': """
Unrealized Currency Gains/Losses (Community)

This module adds a wizard-based report that mimics the Enterprise
"Unrealized Currency Gains/Losses" report, using only Odoo 18
Community features.

- Lists open foreign-currency receivable/payable/bank items
- Shows balances at operation rate vs. current rate
- Computes unrealized FX adjustment per line and total
    """,
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_unrealized_fx_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
