# FlowCredit: Flow-Based Micro-Lending Rails for MSMEs

FlowCredit is an open, protocol-based credit infrastructure designed to unlock formal working capital for India's 63M+ micro-merchants using the **RBI Account Aggregator (AA)** framework and **NPCI Variable UPI AutoPay** rails.

---

## Core Problem Solved
Traditional MSME lending relies on fixed collaterals, ITRs, and fixed-date monthly EMIs. Existing fintech aggregators (BharatPe, Paytm) lock merchants into proprietary QR codes and execute rigid Equated Daily Installments (EDIs). When sales dry up, mandates bounce, imposing ₹350–₹500 penalties on vulnerable merchants. FlowCredit eliminates hardware lock-in and implements elastic, sales-linked repayment sweeps.

---

## Technical Architecture & Core Flow
[ Merchant App ]
│ (1. Scoped Read Consent)
▼
[ Account Aggregator Bridge (AA / ReBIT Schema) ]
│ (2. 90-Day Banking & Cash-Flow Telemetry)
▼
[ FlowCredit Underwriting Engine ] ──> Evaluates RSI, FCF, & Payer Stickiness
│ (3. Sanction & Limit Matrix)
▼
[ Lending Partner Bank Core ] ───────> Disburses via IMPS/UPI (₹5,000 - ₹1,00,000)
│ (4. AutoPay Mandate Registration)
▼
[ NPCI UPI AutoPay Variable Switch ] ──> Dynamic EOD Sweep (5%-10% of Daily Sales, ₹0 on zero sales)

---

## Key Risk & Regulatory Guardrails Built In
1. **RBI Digital Lending Guidelines (DLG) Aligned:** Zero screen-scraping. Data ingestion travels over encrypted AA rails with explicit, purpose-coded consent artefacts. Disbursals flow directly from the Bank balance sheet to the merchant's VPA.
2. **True Reducing-Balance Per Diem Interest:** Interest accrues strictly per day on outstanding principal ($P \times r / 365$). Sweeps apply to accumulated interest first, with the remainder knocking down principal.
3. **Living-Floor Cushion:** If daily retail volume drops below ₹500, the AutoPay sweep automatically sets execution to ₹0 to protect merchant working capital.
4. **Adaptive Anti-Sybil & Persona Profiling:** A rigid transaction floor excludes genuine street vendors. FlowCredit analyzes the median ticket size during AA ingestion to assign a Unique Persona ID (e.g., `PROFILE_MICRO_VENDOR`). The anti-fraud floor dynamically drops to ₹10 for micro-merchants while scaling up for larger retailers, capturing legitimate ₹10–₹40 sales and protecting street stalls without exposing the system to automated ₹1 ping inflation.
5. **Shop Closure Protocol:** Non-performing facilities transition through automated restructuring (Day 15), secondary account sweep (Day 30), and bureau NPA reporting (Day 90) backed by **CGFMU 75% sovereign default guarantee cover**.

---

## REST API Specification
- `POST /api/v1/consent/initiate` - Initiates AA consent request for merchant statement ingestion.
- `POST /api/v1/underwrite/evaluate` - Ingests statement telemetry; returns RSI score, credit limit, and sweep rate.
- `POST /api/v1/mandate/create` - Registers NPCI UPI AutoPay mandate with designated ceiling cap.
- `POST /api/v1/loan/disburse` - Triggers direct banking disbursement to merchant VPA.
- `POST /api/v1/repay/daily-sweep` - Webhook executing dynamic EOD percentage deductions.
- `POST /api/v1/repay/prepay` - Merchant-initiated one-time principal paydown with zero prepayment penalties.