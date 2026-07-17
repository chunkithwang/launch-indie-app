---
name: launch-indie-ios-app
description: Plan, schedule, compress, execute, or audit an indie iOS App Store launch from 45 days before release through 60 days after. Use when a user asks for an iOS launch checklist, dated launch calendar, App Store submission plan, TestFlight or pre-order runway, launch-day plan, post-launch follow-through, ASO/Apple Ads follow-up, or an audit of whether an app is ready to ship. Also use when adapting the Kickstart “ultimate indie iOS app launch checklist” to a real app or ship date.
---

# Launch an Indie iOS App

Turn a ship date into a practical 106-day launch program: day -45 through day +60, including launch day. Treat launch as a sustained operating window, not a single announcement.

## Start with the launch context

Collect or infer the minimum facts needed to make the plan concrete:

- Target release date and today's date.
- Supported Apple platforms and device families.
- App category, audience, one-sentence value proposition, business model, and target territories.
- Current build, TestFlight, App Store Connect, website, metadata, and review status.
- Available launch channels: mailing list, social accounts, press, Product Hunt, directories, and paid acquisition.
- Team, owners, budget, fixed events, and non-negotiable constraints.

If the ship date is missing, ask for it before creating a dated calendar. If the user only wants an audit, proceed without a ship date and report readiness by phase.

## Load the right resources

- Read `references/launch-tasks.json` whenever producing, compressing, or auditing a plan. It is the canonical set of 40 tasks and their original offsets.
- Read `references/apple-requirements.md` before stating App Store limits, TestFlight rules, pre-order windows, review behavior, screenshot sizes, or review-prompt behavior. Apple rules are date-sensitive.
- Read `references/retrospective-lessons.md` when prioritizing scope, beta duration, pre-orders, feedback handling, launch follow-through, or tradeoffs under time pressure.
- Read `references/source-coverage.md` only when checking fidelity to the source article or explaining what “complete” includes.

Do not substitute a generic SaaS launch checklist. Preserve iOS-specific gates such as App Store Connect, TestFlight App Review, product-page assets, app review information, pre-orders, release settings, ratings, ASO, and Apple Ads economics.

## Build the canonical calendar

Generate deterministic dates from the release date:

```bash
python3 scripts/build_launch_plan.py --ship-date 2026-09-15 --format markdown
```

Use `--today YYYY-MM-DD` to make overdue and upcoming status reproducible. Use `--format csv` or `--format json` when the result will be imported into another tool.

Keep every canonical task ID in the plan. Mark a task `not applicable` with a reason instead of deleting it. Examples include Product Hunt for an app with no relevant audience there, iPad screenshots for an iPhone-only app, or Apple Ads when unit economics do not support paid acquisition.

## Tailor without breaking dependencies

Preserve these dependency chains:

1. Positioning -> competitors -> keywords -> metadata -> screenshots, description, pitches, and launch copy.
2. App Store Connect record -> complete metadata and review information -> submitted build -> approval -> pre-order or release.
3. TestFlight build -> tester feedback -> fixes -> reviewed release candidate -> launch freeze.
4. Website and audience building -> pre-order link -> social proof and press kit -> outreach -> launch distribution.
5. Central feedback log -> critical fix -> tested 1.0.1 -> well-timed review prompt -> ASO baseline -> later optimization.
6. Conversion and lifetime-value data -> maximum acquisition cost -> Apple Ads decision.

Do not schedule writing, asset creation, or feature work on launch day when it can be completed beforehand. Reserve day 0 for release operations, publishing prepared material, monitoring, support, and replies.

## Compress a short runway

When fewer than 45 days remain, do not move all overdue tasks blindly to today. Triage them in this order:

1. **Release blockers:** App Store Connect record, privacy and age-rating data, support URL, reviewer notes and demo access, build readiness, TestFlight/App Review, release settings, pricing, and required screenshots.
2. **Message and conversion:** value proposition, audience, competitors, keywords, name, subtitle, description, first three screenshots, website, and download/pre-order call to action.
3. **Lead-time distribution:** featuring nomination if still timely, beta feedback, pre-order, press outreach, social proof, press kit, mailing list, and prepared launch copy.
4. **Optional amplification:** Product Hunt, additional directories, extra screenshots, and paid acquisition.
5. **Post-launch system:** feedback log, review responses, 1.0.1 criteria, review prompt, ASO baseline, update cadence, and retrospective.

Show the original target date beside every compressed date so the user can see what was sacrificed. Flag gates that cannot realistically be compressed rather than implying certainty.

## Run the launch

Before day 0, confirm:

- The approved build and intended release setting are correct.
- Store metadata, availability, price, privacy disclosures, age rating, support URL, reviewer information, and required assets are complete.
- Website, email, social posts, launch article, press kit, Product Hunt materials if applicable, and standard replies are prepared.
- Monitoring, support, analytics, crash reporting, feedback capture, and rollback or hotfix ownership are ready.
- Last-minute feature work is frozen unless it resolves a release blocker.

On day 0, release or verify the pre-order transition, switch the website to a download CTA, publish prepared messages, activate selected channels, monitor health, and reply promptly. Do not let launch-day coding displace customer support unless a critical defect requires it.

## Operate the post-launch window

Centralize all reviews, support mail, social replies, TestFlight feedback, crashes, and analytics. Prioritize repeated patterns and severity over the loudest single request.

Ship 1.0.1 only when it contains a tested fix or meaningful improvement. Ask for ratings after a successful user moment, never on first launch or during onboarding. Establish keyword rankings at day +14, revisit the store page with real data around day +21, evaluate Apple Ads only after calculating conversion and net lifetime value, and carry lessons into the next update at day +60.

## Produce an auditable deliverable

Return the result in the user's language and include:

1. Release date, runway length, launch mode (`canonical` or `compressed`), and overall readiness.
2. A dated task table with canonical task ID, owner, status, dependencies, evidence or done criterion, and risk.
3. A critical-path view of App Store/TestFlight gates.
4. The next seven days of work, ordered by urgency and dependency.
5. Explicit `not applicable`, blocked, and overdue items with reasons.
6. Post-launch checkpoints through day +60.
7. Source links for date-sensitive Apple rules.

Do not claim readiness from a green summary alone. Verify each blocking item with evidence such as App Store Connect status, accepted build, working URLs, current assets, tester results, approved metadata, or measured funnel data.

## Maintain source fidelity

Treat the Kickstart article as the planning framework and Apple documentation as the authority for platform rules. When the two differ, preserve the article's intent but follow current Apple requirements. Mention that adaptation when it changes the user's plan.

The source material is paraphrased and operationalized rather than reproduced verbatim. See `references/source-coverage.md` for the section-by-section completeness audit.
