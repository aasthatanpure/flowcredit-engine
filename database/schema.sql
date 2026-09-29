CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(150) NOT NULL,
    vpa VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    persona_id VARCHAR(50) DEFAULT 'PROFILE_STANDARD_KIRANA',
    current_tier VARCHAR(30) DEFAULT 'TIER_1_STARTER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE aa_consents (
    id SERIAL PRIMARY KEY,
    merchant_id INT REFERENCES merchants(id),
    consent_handle VARCHAR(100) UNIQUE NOT NULL,
    fip_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    valid_until TIMESTAMP NOT NULL
);

CREATE TABLE loan_facilities (
    id SERIAL PRIMARY KEY,
    merchant_id INT REFERENCES merchants(id),
    sanctioned_amount NUMERIC(10, 2) NOT NULL,
    principal_balance NUMERIC(10, 2) NOT NULL,
    unpaid_interest NUMERIC(10, 2) DEFAULT 0.00,
    apr_rate NUMERIC(5, 4) DEFAULT 0.2200,
    daily_sweep_percentage NUMERIC(4, 2) DEFAULT 0.08,
    daily_mandate_ceiling NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE, DELINQUENT, CLOSED
    disbursed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_sweep_ledger (
    id SERIAL PRIMARY KEY,
    loan_id INT REFERENCES loan_facilities(id),
    date DATE NOT NULL,
    daily_inflow_detected NUMERIC(10, 2) NOT NULL,
    amount_swept NUMERIC(10, 2) NOT NULL,
    interest_component NUMERIC(10, 2) NOT NULL,
    principal_component NUMERIC(10, 2) NOT NULL,
    closing_principal NUMERIC(10, 2) NOT NULL,
    execution_status VARCHAR(20) DEFAULT 'SUCCESS'
);