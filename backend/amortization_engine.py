class LoanAmortizationEngine:
    def __init__(self, principal: float, apr: float = 0.22, sweep_pct: float = 0.08, mandate_cap: float = 500.0):
        self.principal = principal
        self.apr = apr
        self.daily_rate = apr / 365.0
        self.sweep_pct = sweep_pct
        self.mandate_cap = mandate_cap
        self.accumulated_interest = 0.0
        self.is_closed = False

    def process_daily_sales(self, daily_retail_sales: float):
        if self.is_closed:
            return {"status": "LOAN_ALREADY_CLOSED", "principal": 0.0}

        # 1. Accrue daily interest on outstanding principal
        today_accrued_interest = self.principal * self.daily_rate
        self.accumulated_interest += today_accrued_interest

        # 2. Living Floor Rule: If sales < 500, zero sweep occurs
        if daily_retail_sales < 500.0:
            return {
                "daily_sales": daily_retail_sales,
                "amount_swept": 0.0,
                "interest_accrued_today": round(today_accrued_interest, 2),
                "total_unpaid_interest": round(self.accumulated_interest, 2),
                "remaining_principal": round(self.principal, 2),
                "note": "Living-floor active (< ₹500). Sweep paused with 0 bounce fees."
            }

        # 3. Compute dynamic sweep and enforce mandate ceiling
        raw_sweep = daily_retail_sales * self.sweep_pct
        effective_sweep = min(raw_sweep, self.mandate_cap)

        # 4. Waterfall: Interest cleared first, then Principal
        interest_deduction = min(effective_sweep, self.accumulated_interest)
        self.accumulated_interest -= interest_deduction

        principal_deduction = effective_sweep - interest_deduction

        if principal_deduction >= self.principal:
            # Overpayment protection
            principal_deduction = self.principal
            self.principal = 0.0
            self.is_closed = True
        else:
            self.principal -= principal_deduction

        return {
            "daily_sales": daily_retail_sales,
            "amount_swept": round(effective_sweep, 2),
            "allocated_to_interest": round(interest_deduction, 2),
            "allocated_to_principal": round(principal_deduction, 2),
            "remaining_unpaid_interest": round(self.accumulated_interest, 2),
            "remaining_principal": round(self.principal, 2),
            "is_closed": self.is_closed
        }