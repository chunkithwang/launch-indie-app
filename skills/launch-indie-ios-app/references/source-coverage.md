# Source coverage audit

## Source set

- Primary article: <https://www.kickstart.tools/blog/the-ultimate-indie-ios-app-launch-checklist>
- Requested anchor: <https://www.kickstart.tools/blog/the-ultimate-indie-ios-app-launch-checklist#the-least-you-need-to-know>
- Linked same-site article: <https://www.kickstart.tools/blog/kickstart-launch-retrospective>
- Primary article publication date: 2026-07-15
- Audit date: 2026-07-17
- Retrieved primary HTML SHA-256: `7f3a002523f4a43bc681bb3bf759cdfc0edd96b49133f47068fc58a1231255f8`
- Retrieved retrospective HTML SHA-256: `ad93d2741bef356d98893df50c4f250ef9246495d26614ddbd2e8edb3cdaf947`

The source text is paraphrased and operationalized. It is not copied verbatim.

## Main-page section mapping

| Source section | Evidence in this Skill |
|---|---|
| The least you need to know | `SKILL.md` launch model, canonical/compressed runway rules, and the 106-day window in `launch-tasks.json` |
| Day -45 to -31: Foundations | `FND-01` through `FND-07` |
| Day -30 to -15: Store presence and beta | `STB-01` through `STB-10` |
| Day -14 to -1: Launch week prep | `LWP-01` through `LWP-06` |
| Day 0: Launch day | `DAY-01` through `DAY-05` |
| Day +1 to +14: Feedback fortnight | `FBF-01` through `FBF-07` |
| Day +15 to +60: Long tail | `LTL-01` through `LTL-05` |
| Before you move on | `SKILL.md` readiness audit, dependency preservation, day-0 support rule, and post-launch checkpoints |

Task count: 7 + 10 + 6 + 5 + 7 + 5 = **40 canonical tasks**. Duplicate offsets such as day -25, day -21, and day 0 are intentionally preserved.

## Page anchors and visual content

All seven navigational anchors are covered: the minimum model plus the six launch phases. The informational meaning of the article's images is retained as:

- Six-phase runway -> phase model and task IDs.
- App Store iceberg -> store metadata plus blocking App Store Connect details.
- Public App Store result -> day-0 availability verification.
- Day-by-day task view -> deterministic schedule script.

The original images are not bundled because they are not required to execute the Skill and remain the publisher's assets.

## Linked page coverage

The main article links to a same-site launch retrospective. `references/retrospective-lessons.md` covers its:

- Reported launch outcomes.
- Successful beta, pre-order, updates, and review practices.
- Scope, burnout, procrastination, and press-outreach failures.
- Five early defect categories and response pattern.
- Feedback and roadmap lessons.
- Four-item action checklist.

The article's Apple links are converted into current platform constraints in `references/apple-requirements.md`, including screenshot specifications, featuring nominations, TestFlight, pre-orders, pre-order analytics, release settings, App Review, expedited review, and rating prompts. Additional first-party Apple pages were used where the article's link did not contain enough implementation detail.

## Deliberate exclusions

- Kickstart product and Mac App Store links are promotional context, not launch methodology.
- Site-wide header/footer links such as Blog, Help, Contact, MCP, and Privacy are navigation chrome, not children of the checklist's knowledge workflow.
- The retrospective's third-party humor link and verbatim customer-review quotations are not operational launch guidance.
- Original prose and images are not reproduced; facts, sequence, rationale, dependencies, and lessons are represented in reusable form.

## Completeness tests

A complete conversion must pass all of these checks:

1. `launch-tasks.json` contains exactly 40 unique IDs spanning offsets -45 through +60.
2. Every source phase maps to an explicit contiguous task-ID range.
3. The schedule script validates the model and emits all 40 tasks in Markdown, CSV, and JSON.
4. Date-sensitive Apple facts have direct first-party links and a verification date.
5. The same-site retrospective has a dedicated, section-complete reference.
6. `SKILL.md` tells an agent when each reference must be read and how to execute canonical, compressed, launch-day, post-launch, and audit workflows.
