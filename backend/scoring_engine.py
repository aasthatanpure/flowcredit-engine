import pandas as pd
import numpy as np

class FlowScoringEngine:
    def __init__(self, txns_csv_path):
        self.df = pd.read_csv(txns_csv_path)
        self.df['date'] = pd.to_datetime(self.df['date'])

    def assign_merchant_profile(self):
        # Find median ticket size to determine merchant category
        all_inflows = self.df[(self.df['type'] == 'INFLOW') & (self.df['category'] == 'UPI_P2M')]
        median_ticket = all_inflows['amount'].median() if len(all_inflows) > 0 else 0.0

        if median_ticket < 50.0:
            return {"profile_id": "PROFILE_MICRO_VENDOR", "anti_sybil_floor": 10.0}
        elif median_ticket <= 300.0:
            return {"profile_id": "PROFILE_STANDARD_KIRANA", "anti_sybil_floor": 50.0}
        else:
            return {"profile_id": "PROFILE_HIGH_TICKET", "anti_sybil_floor": 100.0}

    def evaluate_merchant(self):
        # 1. Dynamically resolve persona ID and threshold floor
        profile = self.assign_merchant_profile()
        threshold = profile["anti_sybil_floor"]

        # 2. Filter genuine customer payments using the dynamic persona floor
        retail_txns = self.df[
            (self.df['type'] == 'INFLOW') & 
            (self.df['category'] == 'UPI_P2M') & 
            (self.df['amount'] >= threshold) &
            (self.df['counterparty'] != 'SELF_CASH')
        ]
        
        # 3. Daily aggregation
        daily_inflows = retail_txns.groupby('date')['amount'].sum()
        mean_daily_sales = daily_inflows.mean() if not daily_inflows.empty else 0.0
        std_daily_sales = daily_inflows.std() if not daily_inflows.empty else 0.0
        
        # Coefficient of Variation (Volatility measure)
        cv = std_daily_sales / mean_daily_sales if mean_daily_sales > 0 else 1.0
        rsi_score = max(0.0, min(100.0, (1.0 - cv) * 100)) # Revenue Stability Index
        
        projected_monthly_gmv = mean_daily_sales * 30
        
        # Limit Matrix Formulation
        if rsi_score >= 60 and projected_monthly_gmv >= 50000:
            sanction_limit = min(projected_monthly_gmv * 0.35, 100000.0)
            sweep_rate = 0.08  # 8%
            tier = "TIER_3_GROWTH"
        elif rsi_score >= 40:
            sanction_limit = min(projected_monthly_gmv * 0.20, 30000.0)
            sweep_rate = 0.08
            tier = "TIER_2_WORKING_CAPITAL"
        else:
            sanction_limit = 5000.0  # Sachet starter loan
            sweep_rate = 0.05
            tier = "TIER_1_STARTER"

        return {
            "persona_id": profile["profile_id"],
            "applied_floor": threshold,
            "tier": tier,
            "rsi_score": round(rsi_score, 2),
            "projected_monthly_gmv": round(projected_monthly_gmv, 2),
            "sanction_limit": round(sanction_limit, -2), # round to hundreds
            "recommended_sweep_pct": sweep_rate,
            "max_daily_mandate_cap": round(mean_daily_sales * 0.20, 2),
            "living_floor_limit": 500.0
        }