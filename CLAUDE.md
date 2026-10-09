# AVP Performance Review — working notes for Claude

Owner: อ๋อง (financial planner, Avenger Planner). Talk to him in Thai.

## What this is
Static web app (PWA) at https://ongiizaaa.github.io/avp-performance-review/ that turns Krungsri / Phillip
fund-transaction exports into his "Performance Review" Excel template (XIRR + time-weighted return).
Hosting: GitHub Pages, "Deploy from a branch" = `main` / `docs` — every push to `main` publishes.
(It moved off Netlify on 2026-10-09 because his free Netlify credits ran out; the old
avp-performance-review.netlify.app copy is frozen.) He wants every change deployed this way —
after editing, always build, test, commit and push to `main`; do not hand him files to upload.

## How to change it
1. Edit `src/app.html` (single source: markup, CSS, JS). Do not hand-edit `docs/index.html` or `docs/sw.js`.
2. `python3 tools/build.py` regenerates `docs/index.html` + `docs/sw.js` (new version stamp each build).
3. Test before pushing (headless Chromium is at /opt/pw-browsers): load `docs/` under a sub-path (it is served from /avp-performance-review/) over a local HTTP
   server, drop sample exports, check the KPIs, download the Excel, and recalc it with LibreOffice
   (`soffice --headless --convert-to xlsx`) to confirm cached formula values match.
4. Commit with a short Thai/English message and push to `main`. Tell him the new version stamp
   shown in the app footer.

## Calculation rules (validated against his hand-made templates — keep them)
- One calculation per account number; never merge Krungsri and Phillip accounts.
- Buy / Switch In / SWI = ซื้อ; Sell / Switch Out / SWO = ขาย; Dividend = ปันผล. Unknown labels are flagged, not guessed.
- Krungsri: date = `Trade Date`, amount = `Amounts`, account = `Cus`.
- Phillip (HTML table saved as .xls): only status `Order Done`; date = `เวลาส่งคำสั่ง` by default
  (matches his template), switchable to `วันลงทุน`; account = `บัญชี`.
- Start value goes to H3, end value to the end-row N cell; formulas mirror his template
  (K cumulative cost, L days, M = $Q$5, N = CF, Q block incl. XIRR). Rows grow with the number of dates.
- `src/template-base.xlsx` is his template with external links removed; chart1 (scatter) is
  re-pointed per export, chartEx1 (waterfall) is left untouched.

## Privacy
Client files are processed in the browser only. Never commit client exports, account numbers,
client names or portfolio values to this repo (it is public).
