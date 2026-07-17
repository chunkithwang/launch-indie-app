# launch-indie-app

[简体中文](README.zh-CN.md)

An open Agent Skill for planning, scheduling, compressing, executing, and auditing indie iOS and macOS launches from day -45 through day +60.

It turns a release date into a 106-day operating plan with 40 dependency-aware tasks. It supports iOS through the App Store and macOS through the Mac App Store, direct Developer ID distribution, or both.

## Highlights

- A validated `SKILL.md` covering iOS, iPadOS, and macOS launch operations.
- Exactly 40 canonical tasks across six launch phases.
- A source-mapped iOS task model with platform-specific macOS overrides.
- A zero-dependency Python calendar generator with iOS/macOS, Mac App Store/direct, and Markdown/CSV/JSON options.
- Current first-party Apple references for App Store rules, Mac App Sandbox, Developer ID, notarization, and universal binaries.
- A section-by-section source coverage audit and a linked launch-retrospective reference.
- Self-contained tests, GitHub Actions CI, and tag-based Release packaging.

## Install in 30 seconds

The [`skills` CLI](https://github.com/vercel-labs/skills) supports Codex, Claude Code, Cursor, OpenCode, and many other agents:

```bash
npx skills add https://github.com/chunkithwang/launch-indie-app --skill launch-indie-app
```

You can also send this prompt to any AI agent with shell access:

```text
Install launch-indie-app by running:
npx skills add https://github.com/chunkithwang/launch-indie-app --skill launch-indie-app
After installation, verify that SKILL.md, references/, and scripts/ exist in the
installed Skill directory, then tell me where it was installed.
```

### Codex GitHub installer (optional)

Codex includes a GitHub installer for public and private repositories:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo chunkithwang/launch-indie-app \
  --path skills/launch-indie-app
```

The Skill becomes available to Codex on the next turn.

### Release ZIP

Download `launch-indie-app-vX.Y.Z.zip` from GitHub Releases, then extract it directly into the agent's global skill directory:

```bash
unzip launch-indie-app-v1.0.0.zip -d ~/.codex/skills
```

The archive intentionally contains one top-level folder named `launch-indie-app`.

## Use

Ask your agent directly:

```text
Use $launch-indie-app to build a dated launch plan for my app. I want to ship on 2026-09-15.
```

For a Mac launch, specify the distribution track:

```text
Use $launch-indie-app to plan my macOS launch for 2026-09-15. I will distribute through both the Mac App Store and a notarized direct download.
```

Or run the deterministic calendar generator:

```bash
python3 skills/launch-indie-app/scripts/build_launch_plan.py \
  --ship-date 2026-09-15 \
  --platform ios \
  --format markdown
```

For macOS, choose `app-store`, `direct`, or `both`:

```bash
python3 skills/launch-indie-app/scripts/build_launch_plan.py \
  --ship-date 2026-09-15 \
  --platform macos \
  --distribution both \
  --format markdown
```

Python 3.9 or later is required only for the bundled calendar script.

## Repository layout

```text
.
├── skills/
│   └── launch-indie-app/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       │   ├── launch-tasks.json
│       │   ├── macos-task-overrides.json
│       │   ├── apple-requirements.md
│       │   ├── macos-distribution.md
│       │   ├── retrospective-lessons.md
│       │   └── source-coverage.md
│       └── scripts/build_launch_plan.py
├── tests/test_skill.py
├── .github/workflows/
├── LICENSE
└── NOTICE
```

Keep repository documentation at the repository root. Do not add README, installation, changelog, or contribution files inside the Skill directory because those files are not runtime guidance.

## Test

No third-party Python packages are required:

```bash
python3 tests/test_skill.py
```

The tests verify frontmatter, folder naming, the six source phase counts, all 40 task IDs and dependencies, macOS override integrity, the -45 to +60 span, and iOS/macOS Markdown/CSV/JSON generation.

## Release a new version

Create and push a version tag from this repository:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The Release workflow validates the Skill, creates an installable ZIP, generates its SHA-256 checksum, and attaches both files to the GitHub Release.

## Attribution and independence

The canonical launch sequence is a paraphrased and operationalized adaptation of Paul Hudson's [“The ultimate indie iOS app launch checklist”](https://www.kickstart.tools/blog/the-ultimate-indie-ios-app-launch-checklist). The macOS task variants are a separate operational adaptation grounded in first-party Apple documentation.

This community project is not affiliated with or endorsed by Paul Hudson, Kickstart, or Apple. It does not redistribute the source article's prose or images. See [NOTICE](NOTICE) and the Skill's source coverage audit for details.

## License

The original code and documentation in this repository are available under the [MIT License](LICENSE). Third-party names, trademarks, linked materials, and source content remain with their respective owners.
