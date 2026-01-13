# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountUnrealizedFxWizard(models.TransientModel):
    _name = 'account.unrealized.fx.wizard'
    _description = 'Unrealized Currency Gains/Losses Wizard'

    date = fields.Date(
        string='Report Date',
        required=True,
        default=fields.Date.context_today,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    include_unposted = fields.Boolean(
        string='Include Unposted Entries',
        default=False,
        help='If enabled, also include unposted journal entries in the report.',
    )
    account_scope = fields.Selection(
        [
            ('receivable_payable', 'Receivable & Payable Only'),
            ('liquidity', 'Bank & Cash Only'),
            ('all', 'All Eligible Balance Sheet Accounts'),
        ],
        string='Accounts To Include',
        required=True,
        default='receivable_payable',
        help='Limit the report to specific account types.',
    )
    line_ids = fields.One2many(
        'account.unrealized.fx.wizard.line',
        'wizard_id',
        string='Lines',
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    total_adjustment = fields.Monetary(
        string='Total Adjustment',
        currency_field='company_currency_id',
        compute='_compute_totals',
        readonly=True,
        store=False,
        help='Sum of all line adjustments in company currency.',
    )

    @api.depends('line_ids.adjustment')
    def _compute_totals(self):
        for wizard in self:
            wizard.total_adjustment = sum(wizard.line_ids.mapped('adjustment'))

    def action_compute_lines(self):
        """Compute unrealized FX lines for open foreign-currency items."""
        self.ensure_one()

        # Clear previously computed lines
        self.line_ids.unlink()

        domain = [
            ('company_id', '=', self.company_id.id),
            ('currency_id', '!=', False),
            ('currency_id', '!=', self.company_currency_id.id),
            ('amount_currency', '!=', 0.0),
            ('account_id.reconcile', '=', True),
            ('reconciled', '=', False),
        ]

        if self.include_unposted:
            domain.append(('move_id.state', 'in', ['draft', 'posted']))
        else:
            domain.append(('move_id.state', '=', 'posted'))

        # Filter by account types (balance sheet only)
        account_types = []
        if self.account_scope in ('receivable_payable', 'all'):
            # Trade receivables & payables
            account_types.extend(['asset_receivable', 'liability_payable'])
        if self.account_scope in ('liquidity', 'all'):
            # Bank & credit card
            account_types.extend(['asset_cash', 'liability_credit_card'])

        if account_types:
            domain.append(('account_id.account_type', 'in', account_types))

        move_lines = self.env['account.move.line'].search(domain, order='date, id')

        lines_vals = []
        for aml in move_lines:
            currency = aml.currency_id
            if not currency:
                continue

            # Foreign balance and company balance at operation rate
            amount_currency = aml.amount_currency
            balance_operation = aml.balance  # company currency at operation date

            # Re-compute at current rate (report date)
            balance_current = currency._convert(
                amount_currency,
                self.company_currency_id,
                self.company_id,
                self.date,
            )

            # Adjustment = Balance at Current Rate - Balance at Operation Rate
            adjustment = balance_current - balance_operation

            vals = {
                'wizard_id': self.id,
                'move_line_id': aml.id,
                'move_id': aml.move_id.id,
                'partner_id': aml.partner_id.id,
                'account_id': aml.account_id.id,
                'date': aml.date,
                'maturity_date': aml.date_maturity,
                'currency_id': currency.id,
                'amount_currency': amount_currency,
                'balance_operation': balance_operation,
                'balance_current': balance_current,
                'adjustment': adjustment,
            }
            lines_vals.append(vals)

        if lines_vals:
            self.env['account.unrealized.fx.wizard.line'].create(lines_vals)

        # Re-open the wizard with computed lines
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.unrealized.fx.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }


class AccountUnrealizedFxWizardLine(models.TransientModel):
    _name = 'account.unrealized.fx.wizard.line'
    _description = 'Unrealized Currency Gains/Losses Line'
    _order = 'date, id'

    wizard_id = fields.Many2one(
        'account.unrealized.fx.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
    )
    move_line_id = fields.Many2one(
        'account.move.line',
        string='Journal Item',
        readonly=True,
    )
    move_id = fields.Many2one(
        'account.move',
        string='Journal Entry',
        readonly=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True,
    )
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        readonly=True,
    )
    date = fields.Date(
        string='Date',
        readonly=True,
    )
    maturity_date = fields.Date(
        string='Maturity Date',
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        readonly=True,
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        related='wizard_id.company_currency_id',
        readonly=True,
        store=False,
    )
    amount_currency = fields.Monetary(
        string='Balance in Foreign Currency',
        currency_field='currency_id',
        readonly=True,
    )
    balance_operation = fields.Monetary(
        string='Balance at Operation Rate',
        currency_field='company_currency_id',
        readonly=True,
    )
    balance_current = fields.Monetary(
        string='Balance at Current Rate',
        currency_field='company_currency_id',
        readonly=True,
    )
    adjustment = fields.Monetary(
        string='Adjustment',
        currency_field='company_currency_id',
        readonly=True,
        help='Balance at Current Rate - Balance at Operation Rate.',
    )
