# MoveInSync Review Intelligence — Executive Recommendations

*Dataset: 3000 written reviews, 2025-09-29 to 2026-10-17. Source: google_play_scraper:in:en:newest. Collected: 2026-10-19T08:23:37Z.*

## 1. Executive summary

- **Displayed Google Play rating:** 4.6401114 (store-wide, all star ratings). **Sample mean of written reviews:** 3.83 (n=3000). These are different metrics.
- **Negative reviews (1–2★):** 809 of 3000 sampled reviews (27.0%).
- **Booking and cancellation** appears in 85 of 809 negative reviews (10.5%); owner type: mixed.
- **Login, authentication and account access** appears in 62 of 809 negative reviews (7.7%); owner type: app.
- **Driver, cab and transport operations** appears in 160 of 809 negative reviews (19.8%); owner type: ops.

Percentages are keyword-rule matches, multi-label (can sum above 100%). Causes below are hypotheses until confirmed with internal telemetry.

## 2. Research question and scope

Why are Play Store ratings for the MoveInSync employee transport app poor, and what should Product and Engineering fix first? Scope: public written reviews only.

## 3. Data sources, collection and sample

- Collection method/status: `google-play-scraper (unofficial)`; country `in`, language `en`, sort `NEWEST`.
- Cleaning: {"input_rows": 3000, "dropped_invalid_rating": 0, "dropped_empty_row": 0, "dropped_duplicates": 0, "missing_text": 0, "missing_date": 0, "missing_version": 291, "output_rows": 3000}
- Selection bias: only users who chose to write a review are included; written reviews skew towards strong opinions and are not representative of all employees or rides.

## 4. Rating and negative-review evidence

| Rating | Count | % of sample (n=3000) |
|---|---|---|
| 1★ | 722 | 24.1% |
| 2★ | 87 | 2.9% |
| 3★ | 78 | 2.6% |
| 4★ | 190 | 6.3% |
| 5★ | 1923 | 64.1% |

Period comparison (last 30 days vs previous 30, anchored 2026-10-17): negative share 26.1% → 29.9% (n=234 → 234).

## 5. Top complaint themes (denominator = 809 negative reviews)

| Theme | Owner type | Count | % of negative |
|---|---|---|---|
| Other or insufficient evidence | n/a | 362 | 44.7% |
| Driver, cab and transport operations | ops | 160 | 19.8% |
| Pickup/drop timing and ETA accuracy | mixed | 90 | 11.1% |
| Booking and cancellation | mixed | 85 | 10.5% |
| Live tracking and GPS accuracy | mixed | 74 | 9.1% |
| Login, authentication and account access | app | 62 | 7.7% |
| UI/UX and navigation | app | 55 | 6.8% |
| Customer support and issue resolution | ops | 53 | 6.6% |
| Crashes, freezing and app stability | app | 52 | 6.4% |
| Performance, speed and loading | app | 39 | 4.8% |
| Safety, OTP and driver verification | ops | 31 | 3.8% |
| Notifications and check-in | app | 30 | 3.7% |
| Route planning and pickup order | ops | 26 | 3.2% |
| Permissions and privacy | app | 6 | 0.7% |

## 6. Representative review evidence

**Booking and cancellation**
- [6663f7b1-7087-45e5-9320-c8a7fbfc6307] 1★, 2026-07-07: “The recent updates in the UI have made the app very difficult to use. Booking a shuttle is now a 2 step process previously it used to be 1. I got confused and thought I had booked a cab while I hadn't. Was too late in realising that. Such major changes need to be released in a better way rather than”
- [941d8a90-37b9-4f3c-93dc-84a6667ddddc] 1★, 2025-12-02: “Many issues with this app. some booking not reflected and not reflecting correctly on the driver's end. Thus making me look like a liar. RESULT? I HAVE 2 DRIVER'S AS AN ENEMY COMPLAINING TO ME. I AM SHOWING THE PROOF I HAVE MADE CORRECT BOOKINGS AND THEY DID NOT EVEN BOTHERED TO LOOK AT IT. AND THEY”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”

**Login, authentication and account access**
- [3e3d8c85-29ba-4636-bb62-ecaf17ffb6c9] 1★, 2026-01-08: “This app is the worst. Not able to login via phone/email as the OTP is not received. The most disgusting thing is, it won't give any message whether the user's mobile/email is registered or not. Without this basic information, how can one know that their details are registered.”
- [4cffdcf2-c19c-4563-b399-0812472c79fd] 1★, 2026-04-15: “Worst user interface. App doesn't even load once you login using your official id. It just says "Something went wrong". Tried uninstalling and installing a couple of times but getting the same error message.”
- [6855f79d-f54e-4ce7-9a7f-213677cec9d1] 1★, 2026-05-13: “Keeps logging out after every 5 to 10 mins of inactivity on the app. Logging in again requires authentication via company's app which is time consuming. Also this poses a problem especially for female passengers who want to report something urgently or send an SOS but are force logged out and have t”

**Driver, cab and transport operations**
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [ab295e36-efc9-4fce-9ed4-638f509c63ef] 1★, 2026-03-02: “The service is extremely disappointing and unreliable. Customer support is useless—the representative who attended my call was rude, unprofessional, and did not attempt to resolve the issue. The app also shows incorrect timings for cab assignment and pickup, which change automatically and cause conf”

**Crashes, freezing and app stability**
- [c43e13cd-0b94-40a0-b3a2-d4c59b14f049] 1★, 2026-04-28: “Worst experience with this app, there is no perfect timing scheduled it changes very badly and when we try to contact the driver no response the auto reply comes (looks like the driver is not responding) and there should be a chat box for me and the driver to connect at least through msg. Please Mov”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”
- [b6720df1-55f7-4ab4-a4f6-6ae7025e91e1] 2★, 2026-01-10: “The Move In Sync app crashes frequently, making it unreliable for daily use. App stability needs serious improvement. It would be very useful to have a feature to add colleagues to Favorites, allowing users to check their login and logout timings and match schedules on a daily, weekly, and monthly b”

**Pickup/drop timing and ETA accuracy**
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [ab295e36-efc9-4fce-9ed4-638f509c63ef] 1★, 2026-03-02: “The service is extremely disappointing and unreliable. Customer support is useless—the representative who attended my call was rude, unprofessional, and did not attempt to resolve the issue. The app also shows incorrect timings for cab assignment and pickup, which change automatically and cause conf”

## 7. Root causes vs hypotheses

Review text alone cannot prove root cause. Every item below is a **hypothesis** with keyword-level evidence; confirmation requires crash, funnel, GPS and notification telemetry from MoveInSync.

## 8. Prioritized fixes and owners

Priority score = frequency % × severity (analyst estimate 1–5) × keyword confidence ÷ effort (S=1, M=2, L=3; analyst estimate).

| # | Theme | Share of negative | Score | Owner | Effort (est.) | Proposed fix | Success metric |
|---|---|---|---|---|---|---|---|
| 1 | Booking and cancellation | 10.5% (85/809) | 13.9 | Product + Backend | M | Review booking/cancellation funnel drop-offs; surface cut-off rules and failure reasons inside the app; reduce steps to book/cancel. | Booking completion rate; cancellation-failure rate (needs internal access) |
| 2 | Login, authentication and account access | 7.7% (62/809) | 13.7 | Backend + Mobile engineering | M | Audit login/OTP/session failure logs; add clear error states and retry; verify SMS/OTP delivery provider success rates. | Login success rate (needs internal access) |
| 3 | Driver, cab and transport operations | 19.8% (160/809) | 12.9 | Operations | L | Route to fleet/vendor management; this is mainly NOT an app defect. | Operations NPS / vendor SLA (needs internal access) |
| 4 | Crashes, freezing and app stability | 6.4% (52/809) | 10.7 | Mobile engineering | M | Pull crash clusters from Play Console Android Vitals / Crashlytics for the app versions named in reviews; reproduce top stack traces; ship a hotfix for top-3 clusters. | Crash-free sessions; ANR rate (needs internal access) |
| 5 | Pickup/drop timing and ETA accuracy | 11.1% (90/809) | 9.3 | Backend + Operations | L | Measure ETA vs actual arrival error; separate algorithm error from late operations; show confidence/ETA ranges. | ETA absolute error p50/p90 (needs internal access) |
| 6 | Live tracking and GPS accuracy | 9.1% (74/809) | 7.8 | Mobile + Backend | L | Compare reported vehicle position with driver-app GPS pings; inspect update interval/staleness; add 'last updated' timestamp. | Position staleness p95; tracking-related complaint share |
| 7 | Customer support and issue resolution | 6.6% (53/809) | 6.6 | Support | M | Measure first-response and resolution time; add in-app issue reporting with ticket status; reply to negative reviews. | First-response time; developer-reply coverage |
| 8 | Safety, OTP and driver verification | 3.8% (31/809) | 6.4 | Operations + Product | M | Triage safety-tagged reviews manually within 48h; confirm driver verification and OTP flows work end-to-end. | Safety incident reports per 10k trips (needs internal access) |
| 9 | Performance, speed and loading | 4.8% (39/809) | 4.8 | Mobile engineering | M | Profile cold start and key screens; cache roster/trip data; measure on low-end devices. | Cold-start time p90; screen load p90 |
| 10 | UI/UX and navigation | 6.8% (55/809) | 4.7 | Product design | M | Run usability review on top-complaint flows after defects are fixed. | Task completion rate in usability tests |
| 11 | Notifications and check-in | 3.7% (30/809) | 4.7 | Mobile + Backend | M | Audit push delivery (FCM) and notification settings flows; handle OEM battery-optimisation kills; add fallback SMS for critical alerts. | Push delivery/open rate (needs internal access) |
| 12 | Route planning and pickup order | 3.2% (26/809) | 2.2 | Operations | L | Review routing rules and pickup sequence complaints with routing team; communicate sequence changes in advance. | Route-related complaint share |
| 13 | Permissions and privacy | 0.7% (6/809) | 1.5 | Product + Legal | S | Review permission prompts and privacy copy; request only needed permissions. | Permission-denial rate |

Baselines for each metric must come from internal data; targets are to be set by the team and are not predictions.

## 9. Action plan

- **First 48 hours:** reproduce the top-3 themes on real devices; pull crash/login/funnel logs for the versions named in reviews; manually triage any safety-tagged reviews.
- **Weeks 1–2:** ship fixes for the highest-confidence app-side defects; reply to negative reviews with specifics; validate via staged rollout.
- **Days 30:** monitor negative-review share and theme shares with the recurring pipeline; check for regressions per release.
- **Ongoing:** weekly pipeline run; investigate flags.

## 10. Metrics and validation

Crash-free sessions, login success, booking completion, ETA error, notification delivery, issue recurrence, negative-review share. Most require internal access. Review-based metrics are measured by this pipeline.

## 11. Risks, assumptions and limitations

- Keyword classification is imprecise; see `reports/methodology.md` for the validation procedure. Classification coverage: 77.1% of reviews matched a category; 44.7% of negative reviews unclassified.
- Reply coverage: {'observable': True, 'overall_pct': 2.9, 'overall_denominator': 3000, 'negative_pct': 4.0, 'negative_denominator': 809}
- No causal claims about releases are made.

## 12. Recurring monitoring

`python -m src.pipeline --collect` (or `--import-csv`) weekly; flags are written to `data/latest_flags.json`.

**Current flags:** 'Other or insufficient evidence' share of negative reviews rose +13.7 pp (37.7% -> 51.4%); 'Crashes, freezing and app stability' share of negative reviews rose +10.5 pp (6.6% -> 17.1%)

## 13. Tools and methodology

Python, pandas, Streamlit, Plotly, pytest; unofficial google-play-scraper or CSV import; rule-based classification; no LLM used.
