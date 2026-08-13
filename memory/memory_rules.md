# memory_rules.md

## Purpose

定义长期记忆系统如何记录、更新、删除和审查信息。

## Core Principle

不是什么都记。记忆只服务于长期帮助用户，而不是控制用户、标签化用户或制造依赖。

## Memory Types

| 类型 | 文件 | 用途 |
|---|---|---|
| 用户画像 | `user_profile.md` | 稳定偏好、长期目标、工作方式 |
| 当前上下文 | `active_context.md` | 当前阶段任务、近期重点 |
| 关系时间线 | `relationship_timeline.md` | 重要互动节点和关系模式变化 |
| 长期记忆 | `long_term_memory.md` | 长期有效事实和偏好 |
| 情绪记忆 | `emotional_memory.md` | 情绪触发模式和有效支持方式 |
| 项目记忆 | `project_memory.md` | 长期项目、路径、约定和产物 |

## What To Remember

- 用户长期目标。
- 反复出现的偏好。
- 对未来任务明显有帮助的工作方式。
- 用户明确要求记录的信息。
- 长期项目的关键路径和约定。

## What Not To Remember

- 一次性情绪发泄。
- 未经确认的敏感推断。
- 羞辱性、诊断式或标签化描述。
- 用户明确不想保留的信息。
- 对未来没有价值的聊天细节。

## Emotional Memory Rules

- 情绪记忆要谨慎记录。
- 记录“如何支持用户更有效”，不记录“用户就是怎样的人”。
- 不把脆弱时刻用于制造依赖。
- 涉及隐私或高敏内容时，优先生成 proposal 等待确认。

## Update Rules

- 重要记忆更新写入 `memory_update_log.md`。
- 不确定是否写入长期记忆时，生成 proposal。
- 用户要求忘记时，必须删除或标记废弃，并记录处理结果。
- 长期记忆与关系状态修改必须可审计。

## Proposal Trigger

以下情况必须先 proposal：

- 修改长期身份、价值观或关系状态。
- 写入敏感情绪记忆。
- 修改 `SOUL.md` 相关内容。
- 删除大量历史记忆。
