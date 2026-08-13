# context_rules.md

## Purpose

定义上下文读取、压缩和会话总结规则。

## Reading Order

1. 默认不要读取所有文件。
2. 先读总规则：`AGENTS.md` 或 `CLAUDE.md`。
3. 再读 `ROUTER.md`。
4. 再按路由读取相关 mode。
5. 再读取相关 memory。
6. 再读取相关 skill。
7. 再读取相关 knowledge。
8. 输出前读取 quality checklist。

## Session End

完成任务后生成 session summary。重要内容进入 memory proposal，不直接污染长期记忆。
