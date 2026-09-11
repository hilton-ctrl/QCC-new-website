# retell-proxy — VENDORED COPY, NOT THE DEPLOYED SOURCE

**Editing files here deploys nothing.**

The live proxy at `https://qcc-retell-proxy.vercel.app` is built by the Vercel
project `qcc-retell-proxy`, which is connected to a **separate GitHub repo**:

    https://github.com/hilton-ctrl/qcc-retell-proxy   (branch: main)

This directory is a copy kept alongside the website for reference. The two were
in sync as of 11 Sept 2026, but nothing enforces that.

## To change the proxy

1. Clone `hilton-ctrl/qcc-retell-proxy`.
2. Make the change there, commit, push to `main`.
3. Vercel auto-deploys on push (confirmed 11 Sept 2026, ~40s).
4. Copy the changed files back here so the two stay in sync.

## Confirming a deploy landed

`OPTIONS` on a route is side-effect free and distinguishes cleanly:

    curl -s -o /dev/null -w "%{http_code}" -X OPTIONS https://qcc-retell-proxy.vercel.app/notify

- `405` — route exists, deploy is live
- `404` — not deployed yet

Do **not** poll with `POST /notify`: every call sends Michael a real email.

## Environment variables

Set in the Vercel project, not here. `RETELL_API_KEY`, `TELNYX_API_KEY`,
`SMTP2GO_API_KEY`. The local `.env` is gitignored reference only and is not
read by the deployed function.

## Related

- `RETELL-TOOL-SETUP.md` — the Retell dashboard tool configs and the SMS revert
- `qcc-llm-prompt-current.md` — the live agent prompt, source of record
- `backups/` — the prompt as it stood before the 11 Sept edits
