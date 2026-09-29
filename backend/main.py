from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FlowCredit Core Engine", version="1.0.0")

class UnderwriteRequest(BaseModel):
    merchant_id: int
    statement_csv_path: str = "merchant_90d_txns.csv"

@app.get("/health")
def health():
    return {"status": "HEALTHY", "rail": "NPCI_AUTOPAY_V2"}

@app.post("/api/v1/consent/initiate")
def initiate_consent(merchant_id: int, vpa: str):
    return {
        "consent_handle": f"consent_req_{merchant_id}_aa",
        "status": "PENDING_MERCHANT_OTP",
        "fip_id": "FIP_HDFC_REBIT"
    }

@app.post("/api/v1/underwrite/evaluate")
def underwrite_merchant(req: UnderwriteRequest):
    from scoring_engine import FlowScoringEngine
    try:
        engine = FlowScoringEngine(req.statement_csv_path)
        return engine.evaluate_merchant()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))