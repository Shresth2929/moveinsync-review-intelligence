# MoveInSync Review Intelligence — Executive Recommendations

*Dataset: 3208 written reviews, 2025-09-29 to 2026-11-21. Source: google_play_scraper:in:en:newest. Collected: 2026-11-23T11:39:49Z.*

## 1. Executive summary

- **Displayed Google Play rating:** 4.6436677 (store-wide, all star ratings). **Sample mean of written reviews:** 3.84 (n=3208). These are different metrics.
- **Negative reviews (1–2★):** 865 of 3208 sampled reviews (27.0%).
- **Booking and cancellation** appears in 89 of 865 negative reviews (10.3%); owner type: mixed.
- **Login, authentication and account access** appears in 66 of 865 negative reviews (7.6%); owner type: app.
- **Driver, cab and transport operations** appears in 175 of 865 negative reviews (20.2%); owner type: ops.

Percentages are keyword-rule matches, multi-label (can sum above 100%). Causes below are hypotheses until confirmed with internal telemetry.

## 2. Research question and scope

Why are Play Store ratings for the MoveInSync employee transport app poor, and what should Product and Engineering fix first? Scope: public written reviews only.

## 3. Data sources, collection and sample

- Collection method/status: `google-play-scraper (unofficial)`; country `in`, language `en`, sort `NEWEST`.
- Cleaning: {"input_rows": 3000, "dropped_invalid_rating": 0, "dropped_empty_row": 0, "dropped_duplicates": 0, "missing_text": 0, "missing_date": 0, "missing_version": 302, "output_rows": 3000}
- Selection bias: only users who chose to write a review are included; written reviews skew towards strong opinions and are not representative of all employees or rides.

## 4. Rating and negative-review evidence

| Rating | Count | % of sample (n=3208) |
|---|---|---|
| 1★ | 768 | 23.9% |
| 2★ | 97 | 3.0% |
| 3★ | 81 | 2.5% |
| 4★ | 201 | 6.3% |
| 5★ | 2061 | 64.2% |

Period comparison (last 30 days vs previous 30, anchored 2026-11-21): negative share 28.8% → 27.8% (n=219 → 180).

## 5. Top complaint themes (denominator = 865 negative reviews)

| Theme | Owner type | Count | % of negative |
|---|---|---|---|
| Other or insufficient evidence | n/a | 384 | 44.4% |
| Driver, cab and transport operations | ops | 175 | 20.2% |
| Pickup/drop timing and ETA accuracy | mixed | 94 | 10.9% |
| Booking and cancellation | mixed | 89 | 10.3% |
| Live tracking and GPS accuracy | mixed | 82 | 9.5% |
| Login, authentication and account access | app | 66 | 7.6% |
| Customer support and issue resolution | ops | 61 | 7.1% |
| UI/UX and navigation | app | 57 | 6.6% |
| Crashes, freezing and app stability | app | 56 | 6.5% |
| Performance, speed and loading | app | 41 | 4.7% |
| Safety, OTP and driver verification | ops | 35 | 4.0% |
| Notifications and check-in | app | 32 | 3.7% |
| Route planning and pickup order | ops | 29 | 3.4% |
| Permissions and privacy | app | 8 | 0.9% |

## 6. Representative review evidence

**Booking and cancellation**
- [6663f7b1-7087-45e5-9320-c8a7fbfc6307] 1★, 2026-07-07: “The recent updates in the UI have made the app very difficult to use. Booking a shuttle is now a 2 step process previously it used to be 1. I got confused and thought I had booked a cab while I hadn't. Was too late in realising that. Such major changes need to be released in a better way rather than”
- [fd4e8200-294d-4877-b4f5-b1e12528ce8d] 1★, 2026-07-15: “does not let you book a bus if location accuracy is off. why do you need location accuracy? are you going to bring the bus to my house? well it does not even let you scan QR code now without location accuracy. thanks guys. any more ways you can make your app more useless?”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”

**Login, authentication and account access**
- [3e3d8c85-29ba-4636-bb62-ecaf17ffb6c9] 1★, 2026-01-08: “This app is the worst. Not able to login via phone/email as the OTP is not received. The most disgusting thing is, it won't give any message whether the user's mobile/email is registered or not. Without this basic information, how can one know that their details are registered.”
- [4cffdcf2-c19c-4563-b399-0812472c79fd] 1★, 2026-04-15: “Worst user interface. App doesn't even load once you login using your official id. It just says "Something went wrong". Tried uninstalling and installing a couple of times but getting the same error message.”
- [7db8a68d-ea44-4449-96c4-c1233f9fcdd6] 1★, 2026-04-21: “I'm unable to login it's fluctuating while I'm opening the app. Just look into this issue”

**Driver, cab and transport operations**
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [7e184ad5-066a-4d36-b7a0-73a0a56bf8a3] 1★, 2026-06-29: “I had a suggestion to add a smart notification feature to remind the user for check-in after the vehicle crosses their pickup point. Sometimes, the vehicle arrives late or we miss by mistake to check-in, then we are marked as "No show" and it comes as a surprise. Introducing this one feature will he”
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”

**Crashes, freezing and app stability**
- [c43e13cd-0b94-40a0-b3a2-d4c59b14f049] 1★, 2026-04-28: “Worst experience with this app, there is no perfect timing scheduled it changes very badly and when we try to contact the driver no response the auto reply comes (looks like the driver is not responding) and there should be a chat box for me and the driver to connect at least through msg. Please Mov”
- [da4ad9ad-acbe-4600-8d32-46883fab9fdd] 1★, 2026-08-31: “There should be an option to directly search for seat number instead of using the map. There should be an option to set default floor in app and portal. Multiple times for multiple people, the seat number (booking shows but without desk allocation) gets removed for bookings which is a major bug”
- [b6720df1-55f7-4ab4-a4f6-6ae7025e91e1] 2★, 2026-01-10: “The Move In Sync app crashes frequently, making it unreliable for daily use. App stability needs serious improvement. It would be very useful to have a feature to add colleagues to Favorites, allowing users to check their login and logout timings and match schedules on a daily, weekly, and monthly b”

**Pickup/drop timing and ETA accuracy**
- [fdc328ac-2980-4425-85ba-86105f68fb3b] 1★, 2025-11-07: “App has very poor logic of setting zoom level and automatically reset it every 30 seconds. When user is waiting for cab at source why you want to keep the destination also in the view? which makes impossible to see how far the cab is. suggestion to keep one point at a time in focus while boarding pi”
- [c158c05c-7985-49cd-bebb-1be703e0ca50] 1★, 2026-06-11: “The GPS tracking system is often unreliable and sometimes shows the driver at an incorrect location, which can lead to unnecessary delays. In addition, the estimated arrival time displayed by the GPS tracker is frequently inaccurate, and the pickup time is rarely synchronized correctly. This has occ”
- [7e184ad5-066a-4d36-b7a0-73a0a56bf8a3] 1★, 2026-06-29: “I had a suggestion to add a smart notification feature to remind the user for check-in after the vehicle crosses their pickup point. Sometimes, the vehicle arrives late or we miss by mistake to check-in, then we are marked as "No show" and it comes as a surprise. Introducing this one feature will he”

## 7. Root causes vs hypotheses

Review text alone cannot prove root cause. Every item below is a **hypothesis** with keyword-level evidence; confirmation requires crash, funnel, GPS and notification telemetry from MoveInSync.

## 8. Prioritized fixes and owners

Priority score = frequency % × severity (analyst estimate 1–5) × keyword confidence ÷ effort (S=1, M=2, L=3; analyst estimate).

| # | Theme | Share of negative | Score | Owner | Effort (est.) | Proposed fix | Success metric |
|---|---|---|---|---|---|---|---|
| 1 | Booking and cancellation | 10.3% (89/865) | 13.6 | Product + Backend | M | Review booking/cancellation funnel drop-offs; surface cut-off rules and failure reasons inside the app; reduce steps to book/cancel. | Booking completion rate; cancellation-failure rate (needs internal access) |
| 2 | Login, authentication and account access | 7.6% (66/865) | 13.5 | Backend + Mobile engineering | M | Audit login/OTP/session failure logs; add clear error states and retry; verify SMS/OTP delivery provider success rates. | Login success rate (needs internal access) |
| 3 | Driver, cab and transport operations | 20.2% (175/865) | 13.1 | Operations | L | Route to fleet/vendor management; this is mainly NOT an app defect. | Operations NPS / vendor SLA (needs internal access) |
| 4 | Crashes, freezing and app stability | 6.5% (56/865) | 11.0 | Mobile engineering | M | Pull crash clusters from Play Console Android Vitals / Crashlytics for the app versions named in reviews; reproduce top stack traces; ship a hotfix for top-3 clusters. | Crash-free sessions; ANR rate (needs internal access) |
| 5 | Pickup/drop timing and ETA accuracy | 10.9% (94/865) | 9.2 | Backend + Operations | L | Measure ETA vs actual arrival error; separate algorithm error from late operations; show confidence/ETA ranges. | ETA absolute error p50/p90 (needs internal access) |
| 6 | Live tracking and GPS accuracy | 9.5% (82/865) | 8.1 | Mobile + Backend | L | Compare reported vehicle position with driver-app GPS pings; inspect update interval/staleness; add 'last updated' timestamp. | Position staleness p95; tracking-related complaint share |
| 7 | Customer support and issue resolution | 7.1% (61/865) | 7.1 | Support | M | Measure first-response and resolution time; add in-app issue reporting with ticket status; reply to negative reviews. | First-response time; developer-reply coverage |
| 8 | Safety, OTP and driver verification | 4.0% (35/865) | 6.7 | Operations + Product | M | Triage safety-tagged reviews manually within 48h; confirm driver verification and OTP flows work end-to-end. | Safety incident reports per 10k trips (needs internal access) |
| 9 | Performance, speed and loading | 4.7% (41/865) | 4.8 | Mobile engineering | M | Profile cold start and key screens; cache roster/trip data; measure on low-end devices. | Cold-start time p90; screen load p90 |
| 10 | Notifications and check-in | 3.7% (32/865) | 4.7 | Mobile + Backend | M | Audit push delivery (FCM) and notification settings flows; handle OEM battery-optimisation kills; add fallback SMS for critical alerts. | Push delivery/open rate (needs internal access) |
| 11 | UI/UX and navigation | 6.6% (57/865) | 4.5 | Product design | M | Run usability review on top-complaint flows after defects are fixed. | Task completion rate in usability tests |
| 12 | Route planning and pickup order | 3.4% (29/865) | 2.3 | Operations | L | Review routing rules and pickup sequence complaints with routing team; communicate sequence changes in advance. | Route-related complaint share |
| 13 | Permissions and privacy | 0.9% (8/865) | 1.9 | Product + Legal | S | Review permission prompts and privacy copy; request only needed permissions. | Permission-denial rate |

Baselines for each metric must come from internal data; targets are to be set by the team and are not predictions.

## 9. Action plan

- **First 48 hours:** reproduce the top-3 themes on real devices; pull crash/login/funnel logs for the versions named in reviews; manually triage any safety-tagged reviews.
- **Weeks 1–2:** ship fixes for the highest-confidence app-side defects; reply to negative reviews with specifics; validate via staged rollout.
- **Days 30:** monitor negative-review share and theme shares with the recurring pipeline; check for regressions per release.
- **Ongoing:** weekly pipeline run; investigate flags.

## 10. Metrics and validation

Crash-free sessions, login success, booking completion, ETA error, notification delivery, issue recurrence, negative-review share. Most require internal access. Review-based metrics are measured by this pipeline.

## 11. Risks, assumptions and limitations

- Keyword classification is imprecise; see `reports/methodology.md` for the validation procedure. Classification coverage: 77.3% of reviews matched a category; 44.4% of negative reviews unclassified.
- Reply coverage: {'observable': True, 'overall_pct': 2.7, 'overall_denominator': 3208, 'negative_pct': 3.8, 'negative_denominator': 865}
- No causal claims about releases are made.

## 12. Recurring monitoring

`python -m src.pipeline --collect` (or `--import-csv`) weekly; flags are written to `data/latest_flags.json`.

**Current flags:** 'Customer support and issue resolution' share of negative reviews rose +9.7 pp (6.3% -> 16.0%)

## 13. Tools and methodology

Python, pandas, Streamlit, Plotly, pytest; unofficial google-play-scraper or CSV import; rule-based classification; no LLM used.
