# ECE OJT targets — ranked from Taft, Malate

All 17 companies in the Mapúa face-to-face OJT masterlist that explicitly list **ECE**, ranked by driving
distance from DLSU–Taft, with the roles each one could plausibly give an electronics engineering student
and what past interns report.

**Live:** https://dynamix14.github.io/ece-ojt-targets/

## What's in it

- 433 masterlist rows screened → 17 list ECE.
- Road distance from Taft (OSRM) + traffic-free drive time, with a caveat that rush hour adds 40–100%.
- Possible ECE internship roles per company, grounded in each employer's own published services.
- **Intern reality** blocks: quoted Indeed / JobStreet intern reviews where they exist (9 of 17), and an
  explicit "no first-hand account found" where they don't.
- Filters by distance band, ECE fit, presence of intern reviews, and whether a live posting exists.
- Contact / MOA details per company in a disclosure panel.

## Caveats carried in the data

- SD Solutions' MOA expires 23 Nov 2026.
- AllHome's slots field contains an Alstom careers URL (masterlist data-entry error).
- APMC's listed email domain is mistyped; Security Bank's email doesn't match the named contact.
- Texas Instruments lists `EECE`, not `ECE` — confirm the code maps to BS Electronics Engineering.
- Some contact emails are from the school masterlist and are shown as-is.

## Structure

- `data.json` — companies, distances, roles, reviews, contacts.
- `build.py` — renders `index.html` from `data.json` (stdlib only).
- `index.html` — the built site.

```bash
python3 build.py
python3 -m http.server
```
