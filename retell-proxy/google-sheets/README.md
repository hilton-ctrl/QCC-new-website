# QCC leads → Google Sheet

One row per **completed call**, written a few seconds after the caller hangs up.

Sheet: **QCC leads**
`https://docs.google.com/spreadsheets/d/1HKRx69Ydy5_SMbvz-oGFoBXJ09CkLwQQ5RSMR89YV4g/edit`

## How it works

```
call ends
  → Retell finishes its post-call analysis
  → POST https://qcc-retell-proxy.vercel.app/retell-webhook   (event: call_analyzed)
  → proxy builds the row
  → POST to the Apps Script web app
  → row appended to the sheet
```

**Why `call_analyzed` and not the moment a booking tool fires:** the enquiry
summary and the outcome do not exist mid-call. A row written while the agent is
still talking could not contain either.

Every call produces a row — the website voice widget, and the outbound callback
the enquiry form triggers, including calls that go to voicemail or are never
answered.

## Columns

| Col | Field | Source |
|---|---|---|
| A | Name | First word of the captured name |
| B | Surname | The rest of it |
| C | Phone no | Dynamic variable, else the call's number, normalised to `04…` |
| D | email | Only if captured in the call — the hero form does not ask for one |
| E | Area/address | Address if the agent got one, else suburb |
| F | Job details | Service discussed |
| G | Enquiry summary | Retell's post-call summary |
| H | Called back y/n | **Guess** — `y` if QCC rang them, `n` for widget calls |
| I | Outcome | **Guess** — Voicemail / No answer / Call failed / Booking requested / Quote requested / Callback requested / Transferred / Enquiry only |
| J | Delegated to | **Guess** — whoever the agent named in the call |
| K | Time | Call start, Brisbane |
| L | Date | Call start, Brisbane |
| M | *(call id)* | De-duplication key. Hide it if you like; **do not delete it** |

**H, I and J are machine guesses.** The sheet is **append-only** — nothing ever
edits a row once written — so when Michael or Jack correct one of those cells,
the correction is permanent and safe.

Column M exists because Retell retries webhooks. Without it, one flaky delivery
becomes two rows for the same call.

## Setup

### 1. Apps Script

1. Open the Apps Script project (either a standalone one, or the sheet's own via
   **Extensions → Apps Script** — the script works in both)
2. Delete the placeholder `function myFunction() {}`, paste `apps-script.gs`
3. `SHARED_SECRET` and `SPREADSHEET_ID` are already filled in
4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Authorise it when prompted (it will warn the app is unverified — expected for
   your own script; choose Advanced → Go to project)
6. Copy the `/exec` URL

"Anyone" is required so Vercel can reach it. The shared secret is what protects
it: without a matching secret the script writes nothing.

To sanity-check before wiring anything up, run `testAppend` from the Apps Script
editor. It writes one obvious test row for you to delete. The first run prompts
for authorisation — the script needs permission to open the spreadsheet.

**Note on standalone projects.** The script opens the sheet with
`SpreadsheetApp.openById(...)`, not `getActiveSpreadsheet()`. The latter returns
null in a standalone project (one created from script.google.com rather than
from the sheet's Extensions menu), which would fail on every write.

### 2. Vercel

In the `qcc-retell-proxy` project → Settings → Environment Variables:

```
SHEETS_WEBHOOK_URL     = https://script.google.com/macros/s/…/exec
SHEETS_SHARED_SECRET   = (same value as SHARED_SECRET in the script)
```

**Then redeploy** — env var changes do not reach a running deployment.

### 3. Retell

Set the agent's webhook URL to:

```
https://qcc-retell-proxy.vercel.app/retell-webhook
```

Agent `agent_a3272ed73666ea736352b563bc` → Webhook settings, or via the API.
The endpoint accepts `call_started` and `call_ended` and ignores them; only
`call_analyzed` writes a row.

## If rows stop appearing

Nothing about this can break a call — a failed sheet write is logged and
swallowed. Check the Vercel function log for:

- `SHEET ROW SKIPPED` — env vars missing
- `SHEET ROW FAILED` — the full row is logged alongside the error, so no lead
  is lost even when the sheet write is

A redeployment of the Apps Script produces a **new** `/exec` URL unless you
deploy to the existing deployment. If you redeploy it fresh, update
`SHEETS_WEBHOOK_URL` and redeploy Vercel.
