import csv
import random
from datetime import datetime, timedelta

def generate_mock_merchant_data(filename="merchant_90d_txns.csv"):
    start_date = datetime.now() - timedelta(days=90)
    txns = []
    
    # Simulating 3 Merchant Personas:
    # 1. Healthy Kirana (Steady 60-100 txns/day)
    # 2. Volatile Salon (Subject to lulls and dry days)
    # 3. Vacation / Closed Store (Has 5-7 consecutive zero-sales days)
    
    unique_customers = [f"cust_{i:04d}@upi" for i in range(1, 400)]
    distributor_vpas = ["distributor_hul@icici", "itc_wholesale@axis", "dairy_supply@kotak"]
    
    current_date = start_date
    for day in range(90):
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Inject vacation/closure on days 70-74
        if 70 <= day <= 74:
            current_date += timedelta(days=1)
            continue
            
        # Daily retail inflows (P2M QR scans)
        daily_count = random.randint(40, 90)
        for _ in range(daily_count):
            amount = round(random.choice([
                random.uniform(20, 100),    # Small items
                random.uniform(100, 500),   # Baskets
                random.uniform(500, 1800)   # Bulk groceries
            ]), 2)
            payer = random.choice(unique_customers)
            txns.append([date_str, "INFLOW", "UPI_P2M", amount, payer, "SUCCESS"])
            
        # Bi-weekly wholesale distributor digital payouts (Outflows)
        if day % 4 == 0:
            outflow_amount = round(random.uniform(8000, 25000), 2)
            distributor = random.choice(distributor_vpas)
            txns.append([date_str, "OUTFLOW", "SUPPLIER_PAY", outflow_amount, distributor, "SUCCESS"])
            
        # Periodic Cash Deposit Machine (CDM) credits (Cash-heavy retail proxy)
        if day % 7 == 0:
            cdm_amount = round(random.uniform(10000, 30000), 2)
            txns.append([date_str, "INFLOW", "CDM_DEPOSIT", cdm_amount, "SELF_CASH", "SUCCESS"])

        current_date += timedelta(days=1)

    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "type", "category", "amount", "counterparty", "status"])
        writer.writerows(txns)

    print(f"Generated {len(txns)} transactions across 90 days in {filename}")

if __name__ == "__main__":
    generate_mock_merchant_data()