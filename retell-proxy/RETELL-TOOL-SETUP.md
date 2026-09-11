# Retell tool swap — SMS alerts → email alerts

**Date:** 11 September 2026
**Status:** temporary. Reverting to SMS once QCC's own Telnyx numbers clear verification.

## Why

The three alert tools were `send_sms` with `sms_sender: current_number`:

- On a **web-widget call** there is no current number, so the alert sent **nothing at all**.
- On the **form callback** the current number is `+61488862843` — Odette's "Baby Bump"
  line — so Michael's lead alerts arrived from a pregnancy-clinic number.

Replacing them with custom functions pointing at the Vercel proxy removes Retell's
dependency on a phone number entirely. The proxy decides how to deliver the alert.

## What to change in the Retell dashboard

Agent `agent_a3272ed73666ea736352b563bc` ("qcc") → **Functions**.

**Delete** these three (all type `send_sms`):

- `send_quote_request`
- `send_callback_request`
- `create_booking_request`

**Add** three **Custom Function** tools using the **same names**. Keeping the names
identical means the agent prompt needs no edits — it already calls these by name.

Common settings for all three:

| Field | Value |
|---|---|
| Type | Custom Function |
| URL | `https://qcc-retell-proxy.vercel.app/notify` |
| Method | POST |
| Speak during execution | off |
| Speak after execution | on |

Leave `transfer_to_human` and `end_call` exactly as they are.

---

### 1. `send_quote_request`

**Description:** Send the customer's quote details through to Michael and Jack. Use after collecting service, suburb, address, job size, name and mobile.

**Parameters (JSON schema):**

```json
{
  "type": "object",
  "properties": {
    "request_type": { "type": "string", "enum": ["quote"], "description": "Always 'quote'." },
    "name":         { "type": "string", "description": "Customer's name." },
    "mobile":       { "type": "string", "description": "Best contact mobile number." },
    "email":        { "type": "string", "description": "Email address, only if the customer wants the quote in writing." },
    "service":      { "type": "string", "description": "Service requested, e.g. carpet cleaning, couch cleaning, bond clean." },
    "suburb":       { "type": "string", "description": "Suburb the job is in." },
    "address":      { "type": "string", "description": "Street address of the job." },
    "job_size":     { "type": "string", "description": "Rooms, stairs, hallways or upholstery items." },
    "notes":        { "type": "string", "description": "Stains, pet odour, access notes, anything else relevant." }
  },
  "required": ["request_type", "name", "mobile", "service", "suburb"]
}
```

### 2. `send_callback_request`

**Description:** Ask Michael or Jack to call the customer back. Use when the question needs a human, or when a tool has failed.

**Parameters (JSON schema):**

```json
{
  "type": "object",
  "properties": {
    "request_type": { "type": "string", "enum": ["callback"], "description": "Always 'callback'." },
    "name":         { "type": "string", "description": "Customer's name." },
    "mobile":       { "type": "string", "description": "Best callback number." },
    "reason":       { "type": "string", "description": "Why a human is needed." },
    "notes":        { "type": "string", "description": "Anything else useful." }
  },
  "required": ["request_type", "name", "mobile", "reason"]
}
```

### 3. `create_booking_request`

**Description:** Send a booking request through to Michael and Jack. Use for straightforward jobs once the details and a preferred day are collected. This is a REQUEST, not a confirmed booking — Michael or Jack confirm the actual time.

**Parameters (JSON schema):**

```json
{
  "type": "object",
  "properties": {
    "request_type":   { "type": "string", "enum": ["booking"], "description": "Always 'booking'." },
    "name":           { "type": "string", "description": "Customer's name." },
    "mobile":         { "type": "string", "description": "Best contact mobile number." },
    "service":        { "type": "string", "description": "Service requested." },
    "suburb":         { "type": "string", "description": "Suburb the job is in." },
    "address":        { "type": "string", "description": "Street address of the job." },
    "preferred_time": { "type": "string", "description": "Preferred day and rough time of day, e.g. 'Friday morning'. Never a confirmed time." },
    "notes":          { "type": "string", "description": "Stains, pet odour, access notes, job size." }
  },
  "required": ["request_type", "name", "mobile", "service", "suburb", "preferred_time"]
}
```

---

## Vercel environment variable

The proxy needs one new variable before any email will send:

```
SMTP2GO_API_KEY = api-xxxxxxxxxxxxxxxx
```

Created 11 Sept 2026 in the SMTP2GO account (Hilton Holder), described
**"QCC website lead alerts"**, scoped to `/email/send` only, default rate limit.
Copy it from **Sending → API Keys** using the Copy button.

### Sender domain

`quick-carpet-cleaners.com.au` is **not** a verified sender in this SMTP2GO
account. Only these are:

| Domain | Status |
|---|---|
| designrepublic.net.au | Verified |
| nevermissacall.net.au | Verified |

So the alert sends from `qcc-website@designrepublic.net.au` and is delivered to
`office@quick-carpet-cleaners.com.au`. Only the sender differs. Sending from an
unverified domain would be rejected — and rejected as HTTP 200 with
`succeeded: 0`, which is exactly why the proxy checks that field.

Free plan has 3 of 5 verified sender slots left. To make the alert self-sent
later, verify `quick-carpet-cleaners.com.au` in SMTP2GO and set:

```
MAIL_FROM = office@quick-carpet-cleaners.com.au
```

**Without `SMTP2GO_API_KEY` nothing breaks** — the alert is logged to the Vercel
function log with the full lead attached, and the call continues normally. But
nobody is notified, so this key is the one thing that makes the feature real.

Note the proxy checks SMTP2GO's `data.succeeded` field, not just the HTTP status:
SMTP2GO answers 200 with `succeeded: 0` when a recipient is rejected, so a status
check alone would log a silent failure as a success.

## Reverting to SMS on Monday

In `api/index.py`:

1. `ALERT_CHANNEL = "sms"` (or `"both"`).
2. `ALERT_SMS_FROM` → QCC's new Telnyx number.
3. `FROM_NUMBER` → the new number as well, so the callback's caller ID stops
   showing the Baby Bump line. (The customer-facing heads-up SMS was removed
   entirely on 11 Sept — don't reinstate it without also updating the hero
   proof strip in `index.html`, which no longer promises a text.)

The Retell tools do **not** need changing — `/notify` honours `ALERT_CHANNEL`
whichever way it is set.

Also still outstanding once the new numbers land: assign one as an **inbound**
number for the `qcc` agent. Right now a lead who misses the callback and rings
back reaches the Baby Bump receptionist.
