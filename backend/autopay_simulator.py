from scoring_engine import FlowScoringEngine
from amortization_engine import LoanAmortizationEngine
import pandas as pd

def run_simulation(csv_path="merchant_90d_txns.csv"):
    # 1. Run Underwriting
    scorer = FlowScoringEngine(csv_path)
    offer = scorer.evaluate_merchant()
    print("--- Underwriting Offer ---")
    for k, v in offer.items():
        print(f"{k}: {v}")

    # 2. Initialize Loan Facility
    engine = LoanAmortizationEngine(
        principal=offer["sanction_limit"],
        apr=0.22,
        sweep_pct=offer["recommended_sweep_pct"],
        mandate_cap=offer["max_daily_mandate_cap"]
    )

    # 3. Simulate Dynamic Sweeps on Inflows
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    daily_sales = df[(df['type'] == 'INFLOW') & (df['category'] == 'UPI_P2M') & (df['amount'] >= 50.0)]
    daily_totals = daily_sales.groupby('date')['amount'].sum().reset_index()

    print("\n--- Simulating First 10 Days of AutoPay Sweeps ---")
    for idx, row in daily_totals.head(10).iterrows():
        res = engine.process_daily_sales(row['amount'])
        print(f"Date: {row['date'].strftime('%Y-%m-%d')} | Inflow: ₹{row['amount']:.2f} | Swept: ₹{res.get('amount_swept', 0.0)} | Bal: ₹{res.get('remaining_principal', 0.0)}")

if __name__ == "__main__":
    run_simulation()