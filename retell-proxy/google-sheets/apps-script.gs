/**
 * QCC leads — Google Sheet writer
 *
 * Set SHARED_SECRET below, then Deploy → New deployment → Web app:
 *
 *   Execute as:      Me
 *   Who has access:  Anyone
 *
 * "Anyone" is required so the Vercel proxy can reach it. The shared secret is
 * what actually protects it — without the matching secret this script writes
 * nothing.
 *
 * Copy the resulting /exec URL into the Vercel project as SHEETS_WEBHOOK_URL.
 *
 * Works in a STANDALONE Apps Script project as well as one bound to the sheet:
 * it opens the spreadsheet by ID rather than relying on getActiveSpreadsheet(),
 * which returns null in a standalone project.
 *
 * Append-only by design. This script never edits an existing row, so anything
 * Michael or Jack type into the sheet is safe from being overwritten.
 */

const SHARED_SECRET = '3vbPHoF4tW5dYjqeYxuW_JQFxTzxYIS7EujjlUB-2tY';

// The "QCC leads" spreadsheet.
const SPREADSHEET_ID = '1HKRx69Ydy5_SMbvz-oGFoBXJ09CkLwQQ5RSMR89YV4g';

function getSheet() {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheets()[0];
}

// Column M holds the Retell call ID. It is the de-duplication key — Retell
// retries webhooks, and without this a flaky delivery would create duplicate
// rows for one call. Safe to hide the column; do not delete it.
const CALL_ID_COLUMN = 13; // M

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    // Two webhook retries can arrive at once; without the lock both would read
    // an empty duplicate check and both would append.
    lock.waitLock(20000);

    if (!e || !e.postData || !e.postData.contents) {
      return json({ ok: false, error: 'empty body' });
    }

    const body = JSON.parse(e.postData.contents);

    if (body.secret !== SHARED_SECRET) {
      return json({ ok: false, error: 'bad secret' });
    }
    if (!Array.isArray(body.row)) {
      return json({ ok: false, error: 'row must be an array' });
    }

    const sheet = getSheet();
    const callId = body.call_id || '';

    if (callId && findCallId(sheet, callId)) {
      return json({ ok: true, skipped: 'duplicate call_id' });
    }

    // Pad/trim to exactly A–L, then put the call id in M.
    const row = body.row.slice(0, 12);
    while (row.length < 12) row.push('');
    row.push(callId);

    sheet.appendRow(row);
    return json({ ok: true, row: sheet.getLastRow() });

  } catch (err) {
    return json({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (ignored) {}
  }
}

function findCallId(sheet, callId) {
  const last = sheet.getLastRow();
  if (last < 2) return false;
  const ids = sheet.getRange(2, CALL_ID_COLUMN, last - 1, 1).getValues();
  for (let i = 0; i < ids.length; i++) {
    if (ids[i][0] === callId) return true;
  }
  return false;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/** Run this once from the editor to confirm the script can write to the sheet. */
function testAppend() {
  const sheet = getSheet();
  sheet.appendRow(['TEST', 'Row', '', '', '', '', 'Delete this row',
                   '', '', '', '', '', 'TEST-' + Date.now()]);
}
