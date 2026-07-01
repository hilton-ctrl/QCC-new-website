from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio, httpx, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quick-carpet-cleaners.com.au",
        "https://www.quick-carpet-cleaners.com.au",
        "http://localhost",
        "http://localhost:5500",
        "http://127.0.0.1",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

AGENT_ID   = "agent_a3272ed73666ea736352b563bc"
FROM_NUMBER = "+61488862843"

# ── Web call (voice widget) ──────────────────────────────────────────────────

@app.post("/create-web-call")
async def create_web_call():
    api_key = os.environ.get("RETELL_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="RETELL_API_KEY not configured")

    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.retellai.com/v2/create-web-call",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"agent_id": AGENT_ID},
            timeout=10,
        )

    if r.status_code != 201:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# ── Outbound call (enquiry form callback) ───────────────────────────────────

class EnquiryForm(BaseModel):
    name:   str
    suburb: str
    mobile: str
    job:    str

@app.post("/create-outbound-call")
async def create_outbound_call(form: EnquiryForm):
    retell_key  = os.environ.get("RETELL_API_KEY")
    telnyx_key  = os.environ.get("TELNYX_API_KEY")
    if not retell_key:
        raise HTTPException(status_code=500, detail="RETELL_API_KEY not configured")
    if not telnyx_key:
        raise HTTPException(status_code=500, detail="TELNYX_API_KEY not configured")

    # Normalise mobile: strip spaces, ensure +61 format
    mobile = form.mobile.strip().replace(" ", "")
    if mobile.startswith("0"):
        mobile = "+61" + mobile[1:]

    sms_body = (
        f"Hi {form.name}, thanks for your enquiry with Quick Carpet Cleaners! "
        f"You'll receive a call from us in the next few seconds. "
        f"Please pick up — it's Mike's team calling about your {form.job}. 🧹"
    )

    async with httpx.AsyncClient() as client:
        # 1. Send SMS via Telnyx
        await client.post(
            "https://api.telnyx.com/v2/messages",
            headers={
                "Authorization": f"Bearer {telnyx_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": FROM_NUMBER,
                "to":   mobile,
                "text": sms_body,
            },
            timeout=10,
        )

        # 2. Wait 10 seconds so customer sees the SMS before the call lands
        await asyncio.sleep(10)

        # 3. Trigger Retell outbound call
        r = await client.post(
            "https://api.retellai.com/v2/create-phone-call",
            headers={
                "Authorization": f"Bearer {retell_key}",
                "Content-Type": "application/json",
            },
            json={
                "from_number": FROM_NUMBER,
                "to_number":   mobile,
                "agent_id":    AGENT_ID,
                "retell_llm_dynamic_variables": {
                    "customer_name":   form.name,
                    "customer_suburb": form.suburb,
                    "job_type":        form.job,
                    "customer_mobile": mobile,
                },
            },
            timeout=10,
        )

    if r.status_code != 201:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return {"status": "sms sent and call initiated"}
