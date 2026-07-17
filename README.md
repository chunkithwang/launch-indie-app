# launch-indie-ios-app

[简体中文](README.zh-CN.md)

An open Agent Skill for planning, scheduling, compressing, executing, and auditing an indie iOS App Store launch from day -45 through day +60.

It turns a release date into a 106-day operating plan with 40 source-mapped tasks covering positioning, App Store Connect, screenshots, TestFlight, pre-orders, press, launch day, feedback, version 1.0.1, ratings, ASO, Apple Ads, and post-launch updates.

## Highlights

- A validated `SKILL.md` compatible with Codex and the open Agent Skills ecosystem.
- Exactly 40 canonical tasks across six launch phases.
- A dependency-aware, machine-readable task model.
- A zero-dependency Python calendar generator with Markdown, CSV, and JSON output.
- Current first-party Apple references for date-sensitive platform rules.
- A section-by-section source coverage audit and a linked launch-retrospective reference.
- Self-contained tests, GitHub Actions CI, and tag-based Release packaging.

## Install

Replace `YOUR_GITHUB_USERNAME` after publishing the repository.

### Universal installer

The [`skills` CLI](https://github.com/vercel-labs/skills) supports Codex, Claude Code, Cursor, OpenCode, and many other agents:

```bash
npx skills add YOUR_GITHUB_USERNAME/launch-indie-ios-app \
  --skill launch-indie-ios-app \
  --global \
  --agent codex \
  --yes
```

Remove `--agent codex` to choose another supported agent interactively.

### Codex GitHub installer

Codex includes a GitHub installer for public and private repositories:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo YOUR_GITHUB_USERNAME/launch-indie-ios-app \
  --path skills/launch-indie-ios-app
```

The Skill becomes available to Codex on the next turn.

### Release ZIP

Download `launch-indie-ios-app-vX.Y.Z.zip` from GitHub Releases, then extract it directly into the agent's global skill directory:

```bash
unzip launch-indie-ios-app-v1.0.0.zip -d ~/.codex/skills
```

The archive intentionally contains one top-level folder named `launch-indie-ios-app`.

## Use

Ask your agent directly:

```text
Use $launch-indie-ios-app to build a dated launch plan for my app. I want to ship on 2026-09-15.
```

Or run the deterministic calendar generator:

```bash
python3 skills/launch-indie-ios-app/scripts/build_launch_plan.py \
  --ship-date 2026-09-15 \
  --format markdown
```

Python 3.9 or later is required only for the bundled calendar script.

## Repository layout

```text
.
├── skills/
│   └── launch-indie-ios-app/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
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

The tests verify frontmatter, folder naming, the six source phase counts, all 40 task IDs and dependencies, the -45 to +60 span, and Markdown/CSV/JSON generation.

## Publish on GitHub

From this repository directory:

```bash
git init
git add .
git commit -m "Initial open-source release"
gh repo create launch-indie-ios-app --public --source=. --remote=origin --push
```

Then replace `YOUR_GITHUB_USERNAME` in both README files and publish the first tagged release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The Release workflow validates the Skill, creates an installable ZIP, generates its SHA-256 checksum, and attaches both files to the GitHub Release.

## Attribution and independence

The launch sequence is a paraphrased and operationalized adaptation of Paul Hudson's [“The ultimate indie iOS app launch checklist”](https://www.kickstart.tools/blog/the-ultimate-indie-ios-app-launch-checklist), with additional links to first-party Apple documentation.

This community project is not affiliated with or endorsed by Paul Hudson, Kickstart, or Apple. It does not redistribute the source article's prose or images. See [NOTICE](NOTICE) and the Skill's source coverage audit for details.

## License

The original code and documentation in this repository are available under the [MIT License](LICENSE). Third-party names, trademarks, linked materials, and source content remain with their respective owners.
