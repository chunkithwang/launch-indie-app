---
name: launch-indie-app
description: Plan, schedule, compress, execute, or audit an indie iOS, iPadOS, or macOS app launch from 45 days before release through 60 days after. Use for App Store launch checklists, dated release calendars, App Store Connect and TestFlight plans, Mac App Store launches, direct macOS distribution with Developer ID and notarization, pre-orders, launch-day operations, post-launch updates, ASO, Apple Ads, or evidence-based ship-readiness audits.
---

# Launch an Indie Apple App

Turn a ship date into a practical 106-day launch program from day -45 through day +60. Support iOS and iPadOS through the App Store, plus macOS through the Mac App Store, direct distribution, or both. Treat launch as a sustained operating window rather than one announcement.

## Start with launch context

Collect or infer the minimum facts needed to make the plan concrete:

- Target platform (`ios` or `macos`), release date, and today's date.
- For macOS, distribution track (`app-store`, `direct`, or `both`), minimum macOS version, and Apple silicon or Intel support.
- App category, audience, one-sentence value proposition, business model, target territories, and localizations.
- Current build, beta, App Store Connect, signing, notarization, website, metadata, and review status as applicable.
- For direct macOS distribution, packaging, payment, licensing, update, download, rollback, and certificate ownership.
- Available launch channels: mailing list, social accounts, press, Product Hunt, directories, and paid acquisition.
- Team, owners, budget, fixed events, and non-negotiable constraints.

Ask for the ship date before creating a dated calendar. Ask for the macOS distribution track when it changes the plan. For a readiness audit, proceed without a date and report evidence by phase and channel.

## Load the right resources

- Read `references/launch-tasks.json` whenever producing, compressing, or auditing a plan. It is the canonical 40-task iOS source model and dependency graph.
- Read `references/macos-task-overrides.json` whenever the target is macOS. It adapts the canonical tasks without changing their IDs, offsets, or dependencies.
- Read `references/apple-requirements.md` before stating App Store limits, screenshot sizes, TestFlight rules, pre-order windows, release behavior, App Review, or rating-prompt behavior.
- Read `references/macos-distribution.md` before planning any macOS launch. Use it to choose a channel and verify sandboxing, Developer ID, Hardened Runtime, notarization, packaging, architecture, update, commerce, and clean-machine test gates.
- Read `references/retrospective-lessons.md` when prioritizing scope, beta duration, pre-orders, feedback handling, launch follow-through, or tradeoffs under time pressure.
- Read `references/source-coverage.md` only when checking fidelity to the source article or explaining what the canonical 40 tasks cover.

Do not substitute a generic SaaS launch checklist. Preserve the platform gates and mark channel-specific work `not applicable` with a reason instead of silently deleting it.

## Select the release track

Use one explicit track:

1. **iOS/iPadOS App Store:** App Store Connect, TestFlight, required device screenshots, App Review, release settings, ratings, ASO, and Apple Ads where relevant.
2. **macOS Mac App Store:** App Sandbox, Mac screenshots, TestFlight for Mac, Mac App Review constraints, store commerce, and Mac App Store-only updates.
3. **macOS direct:** Developer ID, Hardened Runtime, nested-code signing, notarization and stapling, trusted download packaging, payments or licensing, and an authenticated update path.
4. **macOS both:** Maintain independent store and direct artifacts, commerce, release controls, smoke tests, rollback steps, and channel-correct user messaging.

Do not describe notarization as App Review. Do not add a license screen or external updater to a Mac App Store build. Do not ask direct-download users to bypass Gatekeeper.

## Build the canonical calendar

Generate deterministic dates from the release date. iOS remains the backward-compatible default:

```bash
python3 scripts/build_launch_plan.py --ship-date 2026-09-15 --platform ios --format markdown
```

Generate a macOS plan for one or both distribution channels:

```bash
python3 scripts/build_launch_plan.py \
  --ship-date 2026-09-15 \
  --platform macos \
  --distribution both \
  --format markdown
```

Use `--today YYYY-MM-DD` to make overdue and upcoming status reproducible. Use `--format csv` or `--format json` for import. Valid macOS distribution values are `app-store`, `direct`, and `both`; macOS defaults to `both` when the flag is omitted.

Keep every canonical task ID. Apply the macOS override and selected-channel guidance before tailoring owners, evidence, and status. Mark a task `not applicable` with a reason when its channel does not apply.

## Tailor without breaking dependencies

Preserve these chains:

1. Positioning -> competitors -> discovery terms -> metadata and product copy -> screenshots, description, pitches, and launch copy.
2. App Store record -> compliance, metadata, review information, and build -> approval -> pre-order or release.
3. Beta build -> tester feedback -> fixes -> verified release candidate -> launch freeze.
4. Website and audience building -> pre-order, waitlist, or early access -> social proof and press kit -> outreach -> launch distribution.
5. Central feedback log -> critical fix -> tested 1.0.1 -> appropriate review request -> discovery baseline -> later optimization.
6. Conversion and lifetime-value data -> maximum acquisition cost -> paid acquisition decision.
7. For direct macOS: signing ownership -> Hardened Runtime and entitlements -> signed final container -> notarization log -> stapled ticket -> clean-machine Gatekeeper test -> stable download and update feed.

Do not schedule writing, asset creation, signing setup, or package design on launch day. Reserve day 0 for release operations, customer-path smoke tests, prepared publishing, monitoring, support, and replies.

## Compress a short runway

When fewer than 45 days remain, do not move every overdue task to today. Triage in this order:

1. **Release blockers:** build readiness, privacy and compliance, required assets, review access, release controls, and pricing. For Mac App Store, include App Sandbox and App Review. For direct macOS, include Developer ID, Hardened Runtime, nested signatures, notarization, stapling, trusted download, and update rollback.
2. **Message and conversion:** value proposition, audience, competitors, discovery terms, name, description, first screenshots, website, compatibility, price, and purchase or download action.
3. **Lead-time distribution:** beta feedback, pre-order or waitlist, featuring nomination, press outreach, social proof, press kit, mailing list, and prepared launch copy.
4. **Optional amplification:** Product Hunt, additional directories, extra screenshots, and paid acquisition.
5. **Post-launch system:** feedback log, support and review responses, 1.0.1 criteria, channel-correct review request, discovery baseline, update cadence, and retrospective.

Show each original target date beside its compressed date. Flag review, certificate, notarization, payment, or compatibility gates that cannot realistically be compressed.

## Run the launch

Before day 0, verify the exact release candidate for each channel.

For App Store channels, confirm the approved build, release setting, store metadata, availability, price, privacy disclosures, age rating, support URL, reviewer information, screenshots, and purchase flow.

For direct macOS, confirm the artifact checksum, Developer ID signatures for all nested code, Hardened Runtime and entitlements, successful notarization log, stapled ticket, HTTPS download, license or payment recovery, stable update feed, clean-user installation, and rollback artifact.

For every macOS launch, test the minimum and current macOS versions, Apple silicon and Intel when promised, fresh install, first launch, permission denial and recovery, relaunch, upgrade, core file and window workflows, sleep and wake, offline behavior, and support links.

On day 0, release each channel, run a real customer purchase or download and first-launch smoke test, switch the website to live actions, publish prepared messages, activate selected channels, monitor health, and reply promptly. Do not let launch-day feature work displace support unless a critical defect requires it.

## Operate the post-launch window

Centralize store reviews, support mail, direct-purchase issues, social replies, beta feedback, crashes, installation failures, update failures, and analytics. Include platform, OS version, architecture, app version, and installation channel in macOS reports.

Ship 1.0.1 only after testing the affected OS, architecture, channel, clean install, and upgrade path. Use Apple's review prompt only for App Store builds; use a transparent testimonial or public-review request for direct customers. Establish discovery baselines at day +14, revisit channel pages around day +21, evaluate paid acquisition only after calculating channel-specific conversion and net lifetime value, and carry lessons into the next update at day +60.

## Produce an auditable deliverable

Return the result in the user's language and include:

1. Platform, macOS distribution track when applicable, release date, runway length, launch mode (`canonical` or `compressed`), and overall readiness.
2. A dated task table with canonical task ID, channel, owner, status, dependencies, evidence or done criterion, and risk.
3. A critical-path view of App Store review gates and, for direct macOS, signing -> notarization -> Gatekeeper -> download/update gates.
4. The next seven days of work, ordered by urgency and dependency.
5. Explicit `not applicable`, blocked, and overdue items with reasons.
6. Platform test matrix and release-artifact evidence.
7. Post-launch checkpoints through day +60.
8. Source links for date-sensitive Apple rules.

Do not claim readiness from a green summary alone. Verify blocking items with evidence such as App Store Connect status, accepted build, notarization result, artifact checksum, signature and entitlement inspection, clean-machine install, working URLs, tester results, approved metadata, purchase restoration, update test, or measured funnel data.

## Maintain source fidelity

Treat the Kickstart iOS article as the canonical planning sequence and Apple documentation as the authority for current platform rules. Treat `macos-task-overrides.json` and `macos-distribution.md` as an operational adaptation, not as claims made by the source article. When sources differ, preserve the launch intent but follow current Apple requirements and identify the adaptation.

The source material is paraphrased and operationalized rather than reproduced verbatim. See `references/source-coverage.md` for the section-by-section audit.
