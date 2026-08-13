---
name: personal-agent-health-check
description: Personal Agent Harness health check for Codex. Use when the user asks to check, audit, lint, sync, or verify the Personal Agent project, especially after changing rules, knowledge indexes, skills, memory policy, or platform adapters.
---

# Personal Agent Health Check

Use this skill only inside `F:\桌面\Personal Agent` or a copied Personal Agent Harness folder.

## Purpose

检查 Harness 是否仍然一致、可读、可维护，重点发现状态漂移、索引遗漏、核心边界被绕过和平台适配失效。

## Required Files

Read in this order:

1. `AGENTS.md`
2. `CODEX.md` if present
3. `STATUS.md`
4. `knowledge/master_index.md`
5. `knowledge/knowledge_rules.md`
6. `quality/response_checklist.md`

## Checks

- `STATUS.md` 是否与真实目录和 Git 状态一致。
- `knowledge/master_index.md` 是否登记成熟知识域。
- 成熟知识域是否有 `index.md`、`log.md`、`wiki/index.md`。
- `AGENTS.md` 是否仍明确禁止自动修改 `persona/SOUL.md`。
- `memory/memory_rules.md` 是否仍要求长期记忆修改走确认或 proposal。
- `.claude/` 和 `.codex/` 的职责是否没有混淆。
- 项目内 `.codex/skills/` 与用户级 `C:\Users\<用户名>\.codex\skills\personal-agent-*` 是否同步。

## Output

用中文输出：

- 总体状态：正常 / 有漂移 / 有风险。
- 已检查内容。
- 发现的问题，按 P0/P1/P2 排序。
- 建议修复动作。
- 明确说明是否修改了文件；默认只检查，不修改。

## Guardrails

- 默认只读；除非用户明确要求修复，否则不要改文件。
- 不要自动修改 `persona/SOUL.md`、长期记忆或关系状态。
- 不要删除原始资料、OCR 产物或 source report。
