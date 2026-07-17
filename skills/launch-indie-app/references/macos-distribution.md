# macOS distribution and launch gates

Verified against Apple Developer documentation on 2026-07-17. Recheck linked sources before shipping because signing, notarization, App Review, and upload requirements can change.

## Contents

- Choose a distribution track
- Mac App Store track
- Direct distribution track
- Dual-channel releases
- macOS release test matrix
- Evidence required before launch

## Choose a distribution track

Record one track before tailoring the calendar:

| Track | Use when | Non-negotiable launch work |
|---|---|---|
| Mac App Store | Store discovery, StoreKit commerce, managed delivery, or App Store trust matters | App Sandbox, App Store Connect metadata, TestFlight or another beta path, App Review, store release controls, and App Store-only updates |
| Direct | The app needs capabilities or commerce outside Mac App Store constraints, or owns its customer relationship | Developer ID signing, Hardened Runtime, notarization, trusted packaging, payment and licensing operations, secure download, and an authenticated update path |
| Both | The audiences or capabilities justify maintaining two channels | Two release artifacts, channel-correct commerce and updates, synchronized versions, parity decisions, and independent smoke tests |

Do not treat the channels as interchangeable packaging. The Mac App Store build cannot use its own license screen, copy protection, or external updater. A direct build needs its own purchase, recovery, update, and trust story.

## Mac App Store track

- Enable App Sandbox. The sandbox entitlement is an App Store requirement for a macOS app submitted to the Mac App Store.
- Request only the file, network, hardware, personal-information, and temporary-exception entitlements the app needs. Entitlements do not replace user permission prompts.
- Follow App Review Guideline 2.4.5: use Xcode-supported packaging, ship a self-contained app bundle, do not request root escalation, do not install shared code, and distribute updates only through the Mac App Store.
- Do not show a license screen, require a license key, implement separate copy protection, or run a separate updater in the Mac App Store build.
- Upload 1-10 Mac screenshots. Apple currently accepts 1280x800, 1440x900, 2560x1600, or 2880x1800 pixels, all at 16:10.
- TestFlight supports macOS. TestFlight for Mac requires a macOS app built with Xcode 13 or later; beta builds remain testable for up to 90 days.
- Complete the shared App Store requirements in `apple-requirements.md`, including privacy, age rating, export compliance when applicable, support URL, review notes, demo access, pricing, pre-order, and release settings.

Sources:

- <https://developer.apple.com/documentation/xcode/configuring-the-macos-app-sandbox/>
- <https://developer.apple.com/app-store/review/guidelines/#hardware-compatibility>
- <https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/>
- <https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/>

## Direct distribution track

### Signing and Hardened Runtime

- Sign apps, plug-ins, helpers, command-line tools, and installer packages distributed outside the Mac App Store with the appropriate Developer ID certificate.
- Use Developer ID Application for apps and executable code. Use Developer ID Installer when distributing a signed installer package.
- Enable Hardened Runtime and declare only required entitlements. Sign every nested executable, include a secure timestamp, and do not ship with `com.apple.security.get-task-allow` enabled.
- Assign certificate ownership and expiry monitoring before launch. A release process that only works with one developer's local keychain is not operationally ready.

Source: <https://developer.apple.com/developer-id/>

### Notarization

- Notarization is an automated malware and code-signing check, not App Review.
- Submit Developer ID-signed software with Xcode or `notarytool`. Apple no longer accepts notarization uploads from `altool` or Xcode 13 and earlier.
- Inspect the notary log instead of treating an upload as success. Staple the returned ticket to the distributed artifact and verify the exact downloaded artifact through Gatekeeper on a clean Mac.
- Apple supports notarizing apps, disk images, flat installer packages, and ZIP archives. Notarize the same final container users will download.
- Mac App Store submissions do not need this separate notarization path because the store submission process performs equivalent security checks.

Sources:

- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/developer-id/>

### Packaging, commerce, and updates

- Choose ZIP, DMG, or PKG based on the installation workflow. Keep the path simple; never tell customers to disable Gatekeeper or use an unsigned fallback.
- Serve downloads and update metadata over HTTPS. Record the release artifact checksum and retain the prior stable artifact for rollback.
- Provide an authenticated update mechanism or a clear manual-update workflow. Separate beta and stable channels and test an upgrade from the current public version.
- Test payment success, cancellation, refunds, license activation and recovery, offline or service-degraded behavior, and webhook failure handling.
- Publish system requirements, supported architectures, minimum macOS version, price, trial terms, privacy policy, support path, and uninstall instructions before launch.

These are operational requirements rather than Apple platform guarantees. Select tools that fit the product, then require evidence from the real production path.

## Dual-channel releases

- Build, sign, and test the Mac App Store and direct artifacts independently. Channel-specific entitlements, commerce, receipts or licensing, and update code must not leak into the wrong build.
- Keep marketing names and version numbers understandable across channels, but record separate build identifiers, artifact hashes, availability, rollout state, and rollback steps.
- Decide feature parity explicitly. If sandbox restrictions create differences, explain them accurately on both product pages and in support documentation.
- Smoke-test purchase, install, first launch, permissions, update, and restoration for each channel on launch day.

## macOS release test matrix

At minimum, test:

- The minimum supported and current shipping macOS versions.
- Apple silicon, plus Intel when Intel is supported. A universal binary can run natively on both architectures; verify all embedded frameworks and helpers contain the promised slices.
- A fresh standard user account with no development certificates, prior containers, cached permissions, or beta receipts.
- Fresh install, first launch, permission denial and later recovery, relaunch, upgrade from the current public version, downgrade or rollback behavior, and uninstall.
- Core workflows involving files, drag and drop, Open/Save panels, menu commands, keyboard navigation, multiple windows, full screen, multiple displays, dark mode, accessibility, sleep and wake, and login items when relevant.
- Offline and degraded-network behavior, crash reporting, update checks, payment or receipt validation, and support links.

Source for universal binaries: <https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary>

## Evidence required before launch

Do not call a macOS release ready until the selected track has evidence for:

1. The exact version, build, artifact, checksum, channel, and release controls.
2. Passing clean-machine install and first-launch tests without bypassing system security.
3. Correct signatures, entitlements, architecture slices, and minimum-OS behavior.
4. App Review approval for the Mac App Store and successful notarization plus stapling for direct distribution.
5. A tested update path from the current public version and a documented rollback path.
6. Working purchase or download, license or receipt restoration, privacy, support, analytics, crash reporting, and alert ownership.
