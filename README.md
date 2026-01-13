# Unrealized Currency Gains & Losses – Community (Odoo 18)

**Module Name:** `account_unrealized_fx_community`  
**Author:** Dina Sarhan  
**Odoo Version:** 18.0 Community  
**License:** LGPL-3  

---

## Overview

Odoo 18 Community Edition does **not** include the *Unrealized Currency Gains/Losses* report that exists in Enterprise.

This module provides a **Community-compatible alternative** that allows accounting teams to **analyze unrealized foreign exchange differences** on open journal items without posting accounting entries.

The module is **read-only**, safe for production use, and fully compliant with Community Edition constraints.

---

## Key Features

- Wizard-based unrealized FX report
- Supports multi-currency environments
- Works with:
  - Receivables
  - Payables
  - Bank accounts
- Calculates:
  - Balance at original transaction rate
  - Balance at current currency rate
  - Unrealized gain or loss per line
- Displays totals for quick review
- No accounting entries are created

---

## Menu Location

Accounting → Reporting → Unrealized Currency Gains/Losses


---

## How It Works

1. Open **Unrealized Currency Gains/Losses** from Accounting reports.
2. Select:
   - Company
   - As-of date
   - Accounts (optional)
3. Odoo fetches all **open journal items** with a foreign currency.
4. For each line, the module computes:
   - Amount at original rate
   - Amount at current rate
   - Difference (Unrealized Gain / Loss)
5. Results are displayed in a structured list with totals.

> This report is analytical only and does **not** post journal entries.

---

## Security & Access Rights

Access is restricted to:

- **Accounting Manager** (`account.group_account_manager`)

Security is handled through standard Odoo access control rules.

---

## Technical Details

### Models

- `account.unrealized.fx.wizard`
- `account.unrealized.fx.wizard.line`

### Dependencies

- `account`

### Compatibility

- Fully compatible with **Odoo 18 Community**
- No Enterprise code or dependencies
- Safe for production environments

---

## Installation

1. Copy the module to your custom addons path

2. Restart the Odoo service.

3. Enable **Developer Mode**.

4. Update the Apps List.

5. Install **Unrealized Currency Gains & Losses – Community**.

---

## Upgrade Notes

- Safe to upgrade
- No data migration required
- Wizard data is transient and auto-cleaned by Odoo

---

## Known Limitations

- Does not create revaluation journal entries
- Values depend on currency rates configured in Odoo
- For automatic posting, a custom extension or Enterprise edition is required

---

## Typical Use Cases

- Month-end FX exposure review
- Management reporting
- Audit preparation
- Validation before manual FX adjustment entries

---

## Possible Extensions

- Automatic FX revaluation journal entries
- Scheduled month-end revaluation
- Export to Excel
- Partner or account-level grouping

---

## Author

**Dina Sarhan**  
Odoo Developer & Implementor  

---

## License

This module is licensed under the **LGPL-3** License.
