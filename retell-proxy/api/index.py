from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx, os, re, json, datetime

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

# ── Lead alerts ──────────────────────────────────────────────────────────────
#
# TEMPORARY (11 Sept 2026): lead alerts go to Michael by EMAIL, not SMS.
#
# The only number on the Retell account that could send an SMS is
# +61488862843, which is Odette's "Baby Bump" line. Alerting Michael from a
# pregnancy-clinic number confuses two separate businesses, so SMS alerting is
# switched off until QCC's own Telnyx numbers clear verification.
#
# TO REVERT once the new numbers exist:
#   1. Set ALERT_CHANNEL = "sms" below and set ALERT_SMS_FROM to the new number.
#   2. In Retell, point the three alert tools back at send_sms (or leave them on
#      the /notify webhook — it honours ALERT_CHANNEL either way).
#   3. Change FROM_NUMBER above to the new number, so the callback's caller ID
#      stops showing the Baby Bump line. Until then the customer sees an
#      unrelated number on their screen; the agent's opening line and the
#      direct number it reads out are the only mitigation.
#   4. Assign the new number as the qcc agent's INBOUND number, so a customer
#      who misses the callback and rings back does not reach Baby Bump.

ALERT_CHANNEL  = "email"                              # "email" | "sms" | "both"
ALERT_EMAIL    = "office@quick-carpet-cleaners.com.au"
ALERT_SMS_TO   = "+61484312966"                       # Michael's mobile
ALERT_SMS_FROM = FROM_NUMBER                          # replace with QCC's own number on revert

# Sent via SMTP2GO's HTTP API (not raw SMTP — an HTTP call survives serverless
# far better than holding an SMTP conversation open).
#
# The sending domain must be verified in SMTP2GO or the send is rejected — and
# quick-carpet-cleaners.com.au is NOT verified there (checked 11 Sept 2026; only
# designrepublic.net.au and nevermissacall.net.au are). So the alert is sent from
# Design Republic's domain and delivered to QCC. Only the sender differs; the
# recipient is always ALERT_EMAIL.
#
# If quick-carpet-cleaners.com.au is verified later, set MAIL_FROM to an address
# at that domain and the alert becomes self-sent.
MAIL_FROM = os.environ.get("MAIL_FROM", "qcc-website@designrepublic.net.au")


async def send_alert_email(subject: str, body: str) -> bool:
    """Email Michael a lead alert. Returns True only if SMTP2GO accepted it.

    Never raises: a failed alert must not take down the call path with it.
    """
    api_key = os.environ.get("SMTP2GO_API_KEY")
    if not api_key:
        print("ALERT EMAIL SKIPPED - SMTP2GO_API_KEY not configured")
        print(f"UNSENT ALERT: {subject}\n{body}")
        return False

    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api.smtp2go.com/v3/email/send",
                headers={
                    "X-Smtp2go-Api-Key": api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "sender":    MAIL_FROM,
                    "to":        [ALERT_EMAIL],
                    "subject":   subject,
                    "text_body": body,
                },
                timeout=10,
            )
    except Exception as exc:
        print(f"ALERT EMAIL FAILED - {exc!r}")
        print(f"UNSENT ALERT: {subject}\n{body}")
        return False

    # SMTP2GO returns 200 with data.succeeded == 0 for a rejected recipient, and
    # 400 for a bad key. Checking the status alone would report a silent failure
    # as a success, so check the body too.
    succeeded = 0
    try:
        succeeded = (r.json().get("data") or {}).get("succeeded", 0)
    except Exception:
        pass

    if r.status_code != 200 or not succeeded:
        print(f"ALERT EMAIL FAILED - {r.status_code} {r.text}")
        print(f"UNSENT ALERT: {subject}\n{body}")
        return False

    return True


async def send_alert_sms(body: str) -> bool:
    """Text Michael a lead alert. Returns True on success. Never raises."""
    telnyx_key = os.environ.get("TELNYX_API_KEY")
    if not telnyx_key:
        print("ALERT SMS SKIPPED - TELNYX_API_KEY not configured")
        return False

    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api.telnyx.com/v2/messages",
                headers={
                    "Authorization": f"Bearer {telnyx_key}",
                    "Content-Type": "application/json",
                },
                json={"from": ALERT_SMS_FROM, "to": ALERT_SMS_TO, "text": body},
                timeout=10,
            )
    except Exception as exc:
        print(f"ALERT SMS FAILED - {exc!r}")
        return False

    if r.status_code >= 300:
        print(f"ALERT SMS FAILED - {r.status_code} {r.text}")
        return False

    return True


async def send_alert(subject: str, body: str) -> bool:
    """Dispatch a lead alert on whichever channel(s) ALERT_CHANNEL selects."""
    sent = False
    if ALERT_CHANNEL in ("email", "both"):
        sent = await send_alert_email(subject, body) or sent
    if ALERT_CHANNEL in ("sms", "both"):
        # SMS has no subject line, so fold it into the body.
        sent = await send_alert_sms(f"{subject}\n{body}") or sent
    return sent


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


# ── Agent-triggered alerts (Retell custom functions) ─────────────────────────
#
# Replaces the three send_sms tools (send_quote_request, send_callback_request,
# create_booking_request), which were bound to sms_sender "current_number" and
# so sent nothing at all on a web call. Retell POSTs {"call": {...}, "args": {...}}.

FIELD_LABELS = [
    ("name",           "Name"),
    ("mobile",         "Mobile"),
    ("email",          "Email"),
    ("service",        "Service"),
    ("suburb",         "Suburb"),
    ("address",        "Address"),
    ("job_size",       "Job size"),
    ("preferred_time", "Preferred day/time"),
    ("reason",         "Reason"),
    ("notes",          "Notes"),
]

REQUEST_TITLES = {
    "quote":    "QUOTE REQUEST",
    "callback": "CALLBACK REQUEST",
    "booking":  "BOOKING REQUEST",
}


@app.post("/notify")
async def notify(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid JSON")

    # Retell nests the function arguments under "args"; tolerate a flat body too.
    args = payload.get("args") if isinstance(payload.get("args"), dict) else payload
    call = payload.get("call") if isinstance(payload.get("call"), dict) else {}

    kind  = str(args.get("request_type", "quote")).lower()
    title = REQUEST_TITLES.get(kind, "ENQUIRY")

    lines = [f"QCC {title} - from the website AI receptionist", ""]
    for key, label in FIELD_LABELS:
        value = args.get(key)
        if value not in (None, "", "unknown"):
            lines.append(f"{label}: {value}")

    call_id = call.get("call_id")
    if call_id:
        lines += ["", f"Retell call: {call_id}"]

    body    = "\n".join(lines)
    who     = args.get("name") or "Website enquiry"
    subject = f"QCC {title}: {who}"

    delivered = await send_alert(subject, body)

    # Always report success to the agent. It has already told the customer the
    # details are going through, and a delivery failure is logged above with the
    # full lead attached - the customer should not be dragged into that.
    return {
        "success": True,
        "delivered": delivered,
        "message": "Details sent to Michael and Jack.",
    }


# ── Google Sheet row (Retell post-call webhook) ─────────────────────────────
#
# Retell calls this with event "call_analyzed" once a call has ended and its
# transcript has been summarised. That timing matters: the enquiry summary and
# the outcome do not exist mid-call, so a row written when the agent fires a
# booking tool could not contain them.
#
# Writes one row per completed call to the "QCC leads" sheet, via an Apps Script
# web app (see google-sheets/apps-script.gs).
#
# APPEND-ONLY. This never edits an existing row. Columns H, I and J are filled
# with a best guess, but the moment Michael or Jack correct one, nothing will
# overwrite it. Retell may retry a webhook, so the Apps Script de-duplicates on
# the call id in column M.

BRISBANE = datetime.timezone(datetime.timedelta(hours=10))  # QLD has no DST

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def _split_name(full):
    """Sheet wants Name and Surname; every source gives one field."""
    parts = (full or "").strip().split()
    if not parts:
        return "", ""
    return parts[0], " ".join(parts[1:])


def _au_mobile(n):
    n = (n or "").strip().replace(" ", "")
    return "0" + n[3:] if n.startswith("+61") else n


def _build_row(call):
    dyn = call.get("retell_llm_dynamic_variables") or {}
    analysis = call.get("call_analysis") or {}
    custom = analysis.get("custom_analysis_data") or {}

    # Everything the agent said and did, as one searchable blob. Used only for
    # best-guess fields — anything load-bearing comes from a structured field.
    blob = json.dumps(call.get("transcript_with_tool_calls") or
                      call.get("transcript") or "", default=str)

    name = custom.get("name") or dyn.get("customer_name") or ""
    first, last = _split_name(name)

    phone = (dyn.get("customer_mobile") or call.get("to_number")
             or call.get("from_number") or "")
    if call.get("direction") == "inbound":
        phone = call.get("from_number") or phone

    email = custom.get("email") or dyn.get("customer_email") or ""
    if not email:
        found = EMAIL_RE.search(blob.replace("\\u0040", "@"))
        # Ignore QCC's own address turning up in the agent's script.
        if found and "quick-carpet-cleaners" not in found.group(0):
            email = found.group(0)

    area = (custom.get("address") or custom.get("suburb")
            or dyn.get("customer_suburb") or "")
    job = custom.get("service") or dyn.get("job_type") or ""

    summary = analysis.get("call_summary") or ""

    # Called back: did QCC ring them, or did they come to us?
    if call.get("call_type") == "web_call":
        called_back = "n"
    else:
        called_back = "y" if call.get("direction") == "outbound" else "n"

    # Outcome, best guess, most specific signal first.
    reason = (call.get("disconnection_reason") or "").lower()
    if call.get("in_voicemail"):
        outcome = "Voicemail"
    elif "dial_no_answer" in reason or "dial_busy" in reason:
        outcome = "No answer"
    elif "dial_failed" in reason or "error" in reason:
        outcome = "Call failed"
    elif "create_booking_request" in blob:
        outcome = "Booking requested"
    elif "send_quote_request" in blob:
        outcome = "Quote requested"
    elif "send_callback_request" in blob:
        outcome = "Callback requested"
    elif "transfer_to_human" in blob:
        outcome = "Transferred"
    elif analysis.get("call_successful") is False:
        outcome = "Not successful"
    elif summary:
        outcome = "Enquiry only"
    else:
        outcome = ""

    # Delegated to: a guess from who the agent named. Expect Michael to correct it.
    has_jack, has_michael = "Jack" in blob, "Michael" in blob
    if has_jack and not has_michael:
        delegated = "Jack"
    elif has_michael or has_jack:
        delegated = "Michael"
    else:
        delegated = ""

    ts = call.get("start_timestamp") or call.get("end_timestamp")
    if ts:
        when = datetime.datetime.fromtimestamp(ts / 1000, BRISBANE)
    else:
        when = datetime.datetime.now(BRISBANE)

    return [
        first,                      # A Name
        last,                       # B Surname
        _au_mobile(phone),          # C Phone no
        email,                      # D email
        area,                       # E Area/address
        job,                        # F Job details
        summary,                    # G Enquiry summary
        called_back,                # H Called back y/n
        outcome,                    # I Outcome
        delegated,                  # J Delegated to
        when.strftime("%H:%M"),     # K Time
        when.strftime("%d/%m/%Y"),  # L Date
    ]


async def append_sheet_row(call):
    """Append one row to the QCC leads sheet. Never raises."""
    url = os.environ.get("SHEETS_WEBHOOK_URL")
    secret = os.environ.get("SHEETS_SHARED_SECRET")
    if not url or not secret:
        print("SHEET ROW SKIPPED - SHEETS_WEBHOOK_URL/SHEETS_SHARED_SECRET not configured")
        return False

    try:
        row = _build_row(call)
    except Exception as exc:
        print(f"SHEET ROW BUILD FAILED - {exc!r}")
        return False

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Apps Script /exec answers with a 302 to script.googleusercontent.com,
            # so redirects must be followed or every write looks like a failure.
            r = await client.post(
                url,
                json={"secret": secret, "call_id": call.get("call_id", ""), "row": row},
                timeout=15,
            )
    except Exception as exc:
        print(f"SHEET ROW FAILED - {exc!r} | row={row}")
        return False

    if r.status_code >= 300 or '"ok":true' not in r.text.replace(" ", ""):
        print(f"SHEET ROW FAILED - {r.status_code} {r.text[:300]} | row={row}")
        return False

    return True


@app.post("/retell-webhook")
async def retell_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid JSON")

    event = payload.get("event")
    call = payload.get("call") or {}

    # Only call_analyzed carries the summary. call_started and call_ended are
    # acknowledged and ignored, or Retell will treat them as failures and retry.
    if event != "call_analyzed":
        return {"received": True, "ignored": event}

    written = await append_sheet_row(call)
    return {"received": True, "sheet_row_written": written}


# ── Outbound call (enquiry form callback) ───────────────────────────────────

class EnquiryForm(BaseModel):
    name:   str
    suburb: str
    mobile: str
    job:    str

@app.post("/create-outbound-call")
async def create_outbound_call(form: EnquiryForm):
    retell_key = os.environ.get("RETELL_API_KEY")
    if not retell_key:
        raise HTTPException(status_code=500, detail="RETELL_API_KEY not configured")
    # TELNYX_API_KEY is no longer required here — this endpoint sends no SMS.
    # It is still used by send_alert_sms() when ALERT_CHANNEL is switched back.

    # Normalise mobile: strip spaces, ensure +61 format
    mobile = form.mobile.strip().replace(" ", "")
    if mobile.startswith("0"):
        mobile = "+61" + mobile[1:]

    # Alert Michael FIRST, before the SMS and the 10s sleep. This function may
    # be killed by the Vercel execution cap before the call is placed; sending
    # the alert up front means the lead survives even when the callback doesn't.
    await send_alert(
        f"QCC WEBSITE ENQUIRY: {form.name}",
        "\n".join([
            "QCC WEBSITE ENQUIRY - from the homepage form",
            "",
            f"Name: {form.name}",
            f"Mobile: {mobile}",
            f"Suburb: {form.suburb}",
            f"Job: {form.job}",
            "",
            "An AI callback to this customer has been triggered.",
        ]),
    )

    # The customer used to get a heads-up SMS here, followed by a 10s sleep so
    # they saw it before the phone rang. Both are removed (11 Sept 2026):
    #
    #   - The text went out from the Baby Bump number, so a carpet-cleaning
    #     customer received an unsolicited SMS from an unrelated business before
    #     any context existed. Worse than no text at all.
    #   - The 10s sleep likely exceeded the Vercel execution cap, killing the
    #     function after the SMS but before the call was ever placed.
    #
    # The call still identifies itself in its opening line, and the agent reads
    # out QCC's real number, so the customer is not left guessing.

    async with httpx.AsyncClient() as client:
        # Trigger Retell outbound call
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
                    "session_type":    "outbound",
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

    return {"status": "call initiated"}
