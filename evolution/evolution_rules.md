# evolution_rules.md

## Purpose

定义 Agent Harness 如何自我进化，避免失控修改。

## Core Principle

允许进化，但不能失控。所有核心变化必须可审计、可回滚、可由用户确认。

## Must Use Proposal

以下修改必须先进入 `evolution/proposals/`：

- 任何 `persona/SOUL.md` 修改。
- 任何核心人格、边界或价值系统修改。
- 任何长期记忆或关系状态修改。
- 任何 companion mode 边界修改。
- 大范围 mode / skill 改写。

## Required Proposal Fields

每个 evolution proposal 必须包括：

- 修改对象。
- 修改原因。
- 修改前内容。
- 修改后内容。
- 风险。
- 是否需要用户确认。

## Approved / Rejected Flow

- 用户确认后，proposal 移入 `evolution/approved/`。
- 用户拒绝后，proposal 移入 `evolution/rejected/`。
- 执行后的结果写入 `evolution/evolution_log.md`。

## Prohibited Actions

- 不允许 Agent 私自重写核心人格。
- 不允许为了迎合短期情绪改变长期边界。
- 不允许静默修改长期记忆。
- 不允许删除历史记录而不留说明。
