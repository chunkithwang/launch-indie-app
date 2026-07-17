# Apple requirements referenced by the launch plan

Verified against Apple Developer documentation on 2026-07-17. These facts can change; check the linked Apple pages again before submission.

## Contents

- App information and metadata
- Screenshots
- Featuring nominations
- TestFlight
- macOS distribution
- Pre-orders and release settings
- App Review and expedited review
- Ratings and review prompts

## App information and metadata

- The localized app name is 2–30 characters; the subtitle is at most 30 characters.
- The keyword field accepts up to 100 bytes. Do not repeat the app or company name, and do not use other apps' or companies' names.
- The description is at most 4,000 characters and does not support HTML.
- A privacy-policy URL is required for iOS and macOS apps. The age rating is required.
- The support URL must be complete and lead to real contact information as required by applicable law.
- If login is required, provide a non-expiring demo account. Use reviewer notes for special setup, test steps, app-specific settings, or extra accounts.

Sources:

- <https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information>

## Screenshots

- Upload 1–10 screenshots per supported device size in JPEG or PNG; images cannot include an alpha channel or transparency.
- For a 6.9-inch iPhone display, accepted portrait sizes currently include 1260×2736, 1290×2796, and 1320×2868 pixels, with landscape orientations reversed. The source article uses 1320×2868 as its recommended master size.
- If the app runs on iPad, 13-inch iPad screenshots are required. Accepted portrait sizes currently include 2064×2752 and 2048×2732 pixels, with landscape orientations reversed.
- Apple can scale accepted large-display screenshots for several smaller display classes, but verify the current table for the exact device coverage before uploading.
- Mac apps require 1–10 screenshots in one accepted 16:10 size: 1280×800, 1440×900, 2560×1600, or 2880×1800 pixels.
- Prioritize the first three screenshots for the main value story even though up to ten are accepted.

Source: <https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications>

## Featuring nominations

- Submit a launch through App Store Connect's Featuring Nominations area when seeking editorial consideration.
- Apple recommends submitting and finalizing the plan at least three weeks before the launch.
- The nomination can include launch timing, markets, platforms, localizations, related events, supplemental materials, pre-order status, and differentiation.

Sources:

- <https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring>
- <https://developer.apple.com/help/app-store-connect/reference/nominations/nominations-template/>

## TestFlight

- Provide a beta description, What to Test information, and a feedback email.
- A TestFlight build is available for up to 90 days.
- Apple currently allows up to 100 internal App Store Connect testers and up to 10,000 external testers.
- Adding the first build of the app to an external group sends it to TestFlight App Review. The first build requires review; later builds may not require a full review.
- Capture sessions, crashes, screenshots, and written tester feedback, then resolve meaningful issues before App Store submission.
- TestFlight supports macOS. TestFlight for Mac requires a macOS app built with Xcode 13 or later.

Source: <https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/>

## macOS distribution

- A Mac App Store app must enable App Sandbox, use appropriate entitlements, follow the additional macOS requirements in App Review Guideline 2.4.5, and distribute updates only through the Mac App Store.
- Software distributed outside the Mac App Store should be signed with the appropriate Developer ID certificate so Gatekeeper can identify the developer.
- Directly distributed software built after June 1, 2019 and signed with Developer ID must be notarized. Use Xcode or `notarytool`, inspect the result, and staple the ticket to the final artifact.
- Notarization is an automated security and code-signing check, not App Review. Mac App Store submissions do not use this separate notarization path.
- Read `macos-distribution.md` for channel selection, packaging, architecture, commerce, update, test-matrix, and launch-gate guidance.

Sources:

- <https://developer.apple.com/documentation/xcode/configuring-the-macos-app-sandbox/>
- <https://developer.apple.com/app-store/review/guidelines/#hardware-compatibility>
- <https://developer.apple.com/developer-id/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>

## Pre-orders and release settings

- For a brand-new app, the release date can currently be 2–180 days after the pre-order is published.
- The app must be submitted and reviewed before its pre-order can be published.
- On release day, the app automatically downloads for people who pre-ordered and Apple sends them a notification.
- Apple does not notify pre-order customers when a release date changes or a pre-order is removed, so communicate changes directly.
- App Store Connect supports manual, automatic, and automatic-no-earlier-than release settings. Use manual release when approval must not trigger an accidental public launch.
- Apple states that pre-order volume can improve early visibility and contribute to stronger chart placement; treat this as a possible platform effect, not a guaranteed outcome for any app.
- App Store Connect Analytics can report net pre-orders, pre-order conversion, fulfilled downloads, territory, device, and acquisition source once the applicable privacy thresholds are met. Use this data to evaluate channels rather than relying on the launch-day total alone.

Sources:

- <https://developer.apple.com/app-store/pre-orders/>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information>
- <https://developer.apple.com/help/app-store-connect-analytics/acquisition/pre-orders/>

## App Review and expedited review

- Complete reviewer contact, notes, special configuration, and demo access; incomplete information can delay or prevent approval.
- Apple reports that most submissions are reviewed quickly, but launch plans should retain margin for deeper review, questions, or rejection.
- Request expedited review only for exceptional circumstances such as a critical bug fix or an app directly tied to an imminent event.
- For a critical bug, include reproduction steps for the problem in the current public version. Do not treat expedited review as the normal release plan.

Sources:

- <https://developer.apple.com/app-store/review/>
- <https://developer.apple.com/app-store/review/guidelines/>

## Ratings and review prompts

- Use Apple's system review prompt rather than a custom rating prompt.
- Ask after meaningful engagement or a successful task, at a natural break that does not interrupt the user.
- Do not ask at first launch or during onboarding.
- The system limits display of the prompt to at most three times per app in a 365-day period; a request is not a guarantee that the prompt appears.
- For modern SwiftUI, use the `requestReview` environment action where appropriate; `SKStoreReviewController` remains relevant for other implementations.
- Reply to reviews concisely and respectfully. Do not include private information, spam, or generic marketing language.

Sources:

- <https://developer.apple.com/documentation/storekit/requesting-app-store-reviews>
- <https://developer.apple.com/app-store/ratings-and-reviews/>
- <https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews>
