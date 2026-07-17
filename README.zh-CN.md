# launch-indie-ios-app

[English](README.md)

一个开源 Agent Skill，用于规划、排期、压缩、执行和审计独立 iOS App 从上线前 45 天到上线后 60 天的完整发布流程。

它把目标发布日期转换成一套包含 40 项任务的 106 天计划，覆盖定位、App Store Connect、截图、TestFlight、预购、媒体沟通、上线日、反馈、1.0.1、评分、ASO、Apple Ads 和后续更新。

## 主要内容

- 兼容 Codex 和开放 Agent Skills 生态的 `SKILL.md`。
- 六个发布阶段、40 项经过校验的标准任务。
- 包含依赖关系的机器可读任务模型。
- 零第三方依赖的 Python 日期生成器，可输出 Markdown、CSV 和 JSON。
- Apple 官方规则引用、原文逐章节覆盖审计及关联复盘文章总结。
- 自包含测试、GitHub Actions CI 和基于 Git Tag 的 Release 打包。

## 安装

发布仓库后，把以下命令中的 `YOUR_GITHUB_USERNAME` 替换成你的 GitHub 用户名。

### 通用安装方式

[`skills` CLI](https://github.com/vercel-labs/skills) 支持 Codex、Claude Code、Cursor、OpenCode 等多种 Agent：

```bash
npx skills add YOUR_GITHUB_USERNAME/launch-indie-ios-app \
  --skill launch-indie-ios-app \
  --global \
  --agent codex \
  --yes
```

如果删除 `--agent codex`，安装器会让用户选择其他受支持的 Agent。

### Codex 自带 GitHub 安装器

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo YOUR_GITHUB_USERNAME/launch-indie-ios-app \
  --path skills/launch-indie-ios-app
```

安装成功后，Skill 会从 Codex 的下一轮对话开始可用。

### Release ZIP 手动安装

从 GitHub Releases 下载 `launch-indie-ios-app-vX.Y.Z.zip`，然后直接解压到 Codex 全局 Skill 目录：

```bash
unzip launch-indie-ios-app-v1.0.0.zip -d ~/.codex/skills
```

ZIP 中只有一个顶层目录：`launch-indie-ios-app`。

## 使用

```text
使用 $launch-indie-ios-app，为我的 iOS App 制定发布日期为 2026-09-15 的完整计划。
```

也可以直接运行确定性的日期生成器：

```bash
python3 skills/launch-indie-ios-app/scripts/build_launch_plan.py \
  --ship-date 2026-09-15 \
  --format markdown
```

只有日期生成器需要 Python 3.9 或更高版本。

## 测试

```bash
python3 tests/test_skill.py
```

测试会检查 Skill frontmatter、目录名称、六个阶段的任务数量、40 个任务 ID、依赖关系、日期跨度，以及 Markdown、CSV、JSON 三种输出。

## 发布到 GitHub

在仓库目录运行：

```bash
git init
git add .
git commit -m "Initial open-source release"
gh repo create launch-indie-ios-app --public --source=. --remote=origin --push
```

把两个 README 中的 `YOUR_GITHUB_USERNAME` 替换完成后，发布第一个版本：

```bash
git tag v1.0.0
git push origin v1.0.0
```

推送 `v*` Tag 后，Release 工作流会自动校验 Skill、生成可直接安装的 ZIP、计算 SHA-256，并把两个文件附加到 GitHub Release。

## 来源与独立性声明

发布顺序基于 Paul Hudson 的[《The ultimate indie iOS app launch checklist》](https://www.kickstart.tools/blog/the-ultimate-indie-ios-app-launch-checklist)进行改写和工作流化，并补充 Apple 官方文档链接。

本项目是独立社区项目，与 Paul Hudson、Kickstart 或 Apple 没有关联，也未获得其背书。项目不重新分发原文或原图。详情见 [NOTICE](NOTICE)。

## 许可证

仓库中的原创代码和文档使用 [MIT License](LICENSE)。第三方名称、商标、链接材料和来源内容仍归各自权利人所有。
