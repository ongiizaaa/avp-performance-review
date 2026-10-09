# AVP Performance Review — working notes for Claude

Owner: อ๋อง (financial planner, Avenger Planner). Talk to him in Thai.

## What this is
Static web app (PWA) at https://avp-performance-review.netlify.app that turns Krungsri / Phillip
fund-transaction exports into his "Performance Review" Excel template (XIRR + time-weighted return).
Netlify project `avp-performance-review` (team `twish-ong`) is linked to this repo: every push to
`main` deploys automatically. He wants every change deployed this way — after editing, always
build, test, commit and push to `main`; do not hand him files to upload.

## How to change it
1. Edit `src/app.html` (single source: markup, CSS, JS). Do not hand-edit `site/index.html` or `site/sw.js`.
2. `python3 tools/build.py` regenerates `site/index.html` + `site/sw.js` (new version stamp each build).
3. Test before pushing (headless Chromium is at /opt/pw-browsers): load `site/` over a local HTTP
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
