# MoveInSync Review Intelligence — Executive Recommendations

*Dataset: 3142 written reviews, 2025-09-29 to 2026-11-07. Source: google_play_scraper:in:en:newest. Collected: 2026-11-09T10:47:12Z.*

## 1. Executive summary

- **Displayed Google Play rating:** 4.6434183 (store-wide, all star ratings). **Sample mean of written reviews:** 3.84 (n=3142). These are different metrics.
- **Negative reviews (1–2★):** 847 of 3142 sampled reviews (27.0%).
- **Booking and cancellation** appears in 88 of 847 negative reviews (10.4%); owner type: mixed.
- **Login, authentication and account access** appears in 65 of 847 negative reviews (7.7%); owner type: app.
- **Driver, cab and transport operations** appears in 168 of 847 negative reviews (19.8%); owner type: ops.

Percentages are keyword-rule matches, multi-label (can sum above 100%). Causes below are hypotheses until confirmed with internal telemetry.

## 2. Research question and scope

Why are Play Store ratings for the MoveInSync employee transport app poor, and what should Product and Engineering fix first? Scope: public written reviews only.

## 3. Data sources, collection and sample

- Collection method/status: `google-play-scraper (unofficial)`; country `in`, language `en`, sort `NEWEST`.
- Cleaning: {"input_rows": 3000, "dropped_invalid_rating": 0, "dropped_empty_row": 0, "dropped_duplicates": 0, "missing_text": 0, "missing_date": 0, "missing_version": 297, "output_rows": 3000}
- Selection bias: only users who chose to write a review are included; written reviews skew towards strong opinions and are not representative of all employees or rides.

## 4. Rating and negative-review evidence

| Rating | Count | % of sample (n=3142) |
|---|---|---|
| 1★ | 753 | 24.0% |
| 2★ | 94 | 3.0% |
| 3★ | 80 | 2.5% |
| 4★ | 196 | 6.2% |
| 5★ | 2019 | 64.3% |

Period comparison (last 30 days vs previous 30, anchored 2026-11-07): negative share 28.1% → 27.2% (n=253 → 213).

## 5. Top complaint themes (denominator = 847 negative reviews)

| Theme | Owner type | Count | % of negative |
|---|---|---|---|
| Other or insufficient evidence | n/a | 379 | 44.7% |
| Driver, cab and transport operations | ops | 168 | 19.8% |
| Pickup/drop timing and ETA accuracy | mixed | 93 | 11.0% |
| Booking and cancellation | mixed | 88 | 10.4% |
| Live tracking and GPS accuracy | mixed | 81 | 9.6% |
| Login, authentication and account access | app | 65 | 7.7% |
| Customer support and issue resolution | ops | 58 | 6.8% |
| UI/UX and navigation | app | 57 | 6.7% |
| Crashes, freezing and app stability | app | 55 | 6.5% |
| Performance, speed and loading | app | 40 | 4.7% |
| Safety, OTP and driver verification | ops | 33 | 3.9% |
| Notifications and check-in | app | 31 | 3.7% |
| Route planning and pickup order | ops | 27 | 3.2% |
| Permissions and privacy | app | 7 | 0.8% |

## 6. Representative review evidence

**Booking and cancellation**
- [6663f7b1-7087-45e5-9320-c8a7fbfc6307] 1★, 2026-07-07: “The recent updates in the UI have made the app very difficult to use. Booking a shuttle is now a 2 step process previously it used to be 1. I got confused and thought I had booked a cab while I hadn't. Was too late in realising that. Such major changes need to be released in a better way rather than”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”
- [fd4e8200-294d-4877-b4f5-b1e12528ce8d] 1★, 2026-07-15: “does not let you book a bus if location accuracy is off. why do you need location accuracy? are you going to bring the bus to my house? well it does not even let you scan QR code now without location accuracy. thanks guys. any more ways you can make your app more useless?”

**Login, authentication and account access**
- [3e3d8c85-29ba-4636-bb62-ecaf17ffb6c9] 1★, 2026-01-08: “This app is the worst. Not able to login via phone/email as the OTP is not received. The most disgusting thing is, it won't give any message whether the user's mobile/email is registered or not. Without this basic information, how can one know that their details are registered.”
- [4cffdcf2-c19c-4563-b399-0812472c79fd] 1★, 2026-04-15: “Worst user interface. App doesn't even load once you login using your official id. It just says "Something went wrong". Tried uninstalling and installing a couple of times but getting the same error message.”
- [288dfb0e-070c-4b36-a624-f22cd76bc386] 1★, 2026-05-28: “not getting the otp to login. i mailed their customer support team multiple times but still no response. very disappointed”

**Driver, cab and transport operations**
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”
- [7e184ad5-066a-4d36-b7a0-73a0a56bf8a3] 1★, 2026-06-29: “I had a suggestion to add a smart notification feature to remind the user for check-in after the vehicle crosses their pickup point. Sometimes, the vehicle arrives late or we miss by mistake to check-in, then we are marked as "No show" and it comes as a surprise. Introducing this one feature will he”

**Crashes, freezing and app stability**
- [c43e13cd-0b94-40a0-b3a2-d4c59b14f049] 1★, 2026-04-28: “Worst experience with this app, there is no perfect timing scheduled it changes very badly and when we try to contact the driver no response the auto reply comes (looks like the driver is not responding) and there should be a chat box for me and the driver to connect at least through msg. Please Mov”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”
- [f7df20ab-fe77-4454-9a07-55438ce28c6e] 1★, 2026-06-24: “terrible phone app... keeps hanging”

**Pickup/drop timing and ETA accuracy**
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”
- [7e184ad5-066a-4d36-b7a0-73a0a56bf8a3] 1★, 2026-06-29: “I had a suggestion to add a smart notification feature to remind the user for check-in after the vehicle crosses their pickup point. Sometimes, the vehicle arrives late or we miss by mistake to check-in, then we are marked as "No show" and it comes as a surprise. Introducing this one feature will he”

## 7. Root causes vs hypotheses

Review text alone cannot prove root cause. Every item below is a **hypothesis** with keyword-level evidence; confirmation requires crash, funnel, GPS and notification telemetry from MoveInSync.

## 8. Prioritized fixes and owners

Priority score = frequency % × severity (analyst estimate 1–5) × keyword confidence ÷ effort (S=1, M=2, L=3; analyst estimate).

| # | Theme | Share of negative | Score | Owner | Effort (est.) | Proposed fix | Success metric |
|---|---|---|---|---|---|---|---|
| 1 | Booking and cancellation | 10.4% (88/847) | 13.7 | Product + Backend | M | Review booking/cancellation funnel drop-offs; surface cut-off rules and failure reasons inside the app; reduce steps to book/cancel. | Booking completion rate; cancellation-failure rate (needs internal access) |
| 2 | Login, authentication and account access | 7.7% (65/847) | 13.7 | Backend + Mobile engineering | M | Audit login/OTP/session failure logs; add clear error states and retry; verify SMS/OTP delivery provider success rates. | Login success rate (needs internal access) |
| 3 | Driver, cab and transport operations | 19.8% (168/847) | 12.9 | Operations | L | Route to fleet/vendor management; this is mainly NOT an app defect. | Operations NPS / vendor SLA (needs internal access) |
| 4 | Crashes, freezing and app stability | 6.5% (55/847) | 11.0 | Mobile engineering | M | Pull crash clusters from Play Console Android Vitals / Crashlytics for the app versions named in reviews; reproduce top stack traces; ship a hotfix for top-3 clusters. | Crash-free sessions; ANR rate (needs internal access) |
| 5 | Pickup/drop timing and ETA accuracy | 11.0% (93/847) | 9.2 | Backend + Operations | L | Measure ETA vs actual arrival error; separate algorithm error from late operations; show confidence/ETA ranges. | ETA absolute error p50/p90 (needs internal access) |
| 6 | Live tracking and GPS accuracy | 9.6% (81/847) | 8.2 | Mobile + Backend | L | Compare reported vehicle position with driver-app GPS pings; inspect update interval/staleness; add 'last updated' timestamp. | Position staleness p95; tracking-related complaint share |
| 7 | Customer support and issue resolution | 6.8% (58/847) | 6.8 | Support | M | Measure first-response and resolution time; add in-app issue reporting with ticket status; reply to negative reviews. | First-response time; developer-reply coverage |
| 8 | Safety, OTP and driver verification | 3.9% (33/847) | 6.5 | Operations + Product | M | Triage safety-tagged reviews manually within 48h; confirm driver verification and OTP flows work end-to-end. | Safety incident reports per 10k trips (needs internal access) |
| 9 | Performance, speed and loading | 4.7% (40/847) | 4.8 | Mobile engineering | M | Profile cold start and key screens; cache roster/trip data; measure on low-end devices. | Cold-start time p90; screen load p90 |
| 10 | Notifications and check-in | 3.7% (31/847) | 4.7 | Mobile + Backend | M | Audit push delivery (FCM) and notification settings flows; handle OEM battery-optimisation kills; add fallback SMS for critical alerts. | Push delivery/open rate (needs internal access) |
| 11 | UI/UX and navigation | 6.7% (57/847) | 4.6 | Product design | M | Run usability review on top-complaint flows after defects are fixed. | Task completion rate in usability tests |
| 12 | Route planning and pickup order | 3.2% (27/847) | 2.2 | Operations | L | Review routing rules and pickup sequence complaints with routing team; communicate sequence changes in advance. | Route-related complaint share |
| 13 | Permissions and privacy | 0.8% (7/847) | 1.6 | Product + Legal | S | Review permission prompts and privacy copy; request only needed permissions. | Permission-denial rate |

Baselines for each metric must come from internal data; targets are to be set by the team and are not predictions.

## 9. Action plan

- **First 48 hours:** reproduce the top-3 themes on real devices; pull crash/login/funnel logs for the versions named in reviews; manually triage any safety-tagged reviews.
- **Weeks 1–2:** ship fixes for the highest-confidence app-side defects; reply to negative reviews with specifics; validate via staged rollout.
- **Days 30:** monitor negative-review share and theme shares with the recurring pipeline; check for regressions per release.
- **Ongoing:** weekly pipeline run; investigate flags.

## 10. Metrics and validation

Crash-free sessions, login success, booking completion, ETA error, notification delivery, issue recurrence, negative-review share. Most require internal access. Review-based metrics are measured by this pipeline.

## 11. Risks, assumptions and limitations

- Keyword classification is imprecise; see `reports/methodology.md` for the validation procedure. Classification coverage: 77.2% of reviews matched a category; 44.7% of negative reviews unclassified.
- Reply coverage: {'observable': True, 'overall_pct': 2.8, 'overall_denominator': 3142, 'negative_pct': 3.9, 'negative_denominator': 847}
- No causal claims about releases are made.

## 12. Recurring monitoring

`python -m src.pipeline --collect` (or `--import-csv`) weekly; flags are written to `data/latest_flags.json`.

**Current flags:** 'Live tracking and GPS accuracy' share of negative reviews rose +9.9 pp (5.6% -> 15.5%); 'Customer support and issue resolution' share of negative reviews rose +9.3 pp (2.8% -> 12.1%)

## 13. Tools and methodology

Python, pandas, Streamlit, Plotly, pytest; unofficial google-play-scraper or CSV import; rule-based classification; no LLM used.
