# Contributing

Contributions that make the launch plan more accurate, current, or useful are welcome.

## Before opening a pull request

1. Keep runtime guidance inside `skills/launch-indie-ios-app/`; keep repository documentation at the repository root.
2. Do not copy prose or images from the source articles. Paraphrase facts, workflow, rationale, and lessons with attribution.
3. Treat Apple Developer documentation as authoritative for platform requirements. Add a first-party URL and update the verification date when changing a date-sensitive rule.
4. Preserve the 40 canonical source tasks unless the primary article changes. If it changes, update the task model, coverage audit, tests, and source verification together.
5. Keep `SKILL.md` concise and route detailed material through one-level-deep files in `references/`.
6. Run the complete test suite.

```bash
python3 tests/test_skill.py
```

## Pull request checklist

- Explain the user-facing behavior that changes.
- Cite the relevant primary source when changing an Apple rule.
- Confirm all tests pass on Python 3.9 or later.
- Confirm no generated caches, local plans, credentials, or source-article copies are included.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
