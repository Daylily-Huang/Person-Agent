# memory_check.md

## Check Items

- 当前任务是否真的需要读取记忆。
- 是否只读取了相关记忆。
- 是否避免伪造用户长期偏好。
- 是否把一次性信息误写成长期记忆。
- 是否需要创建 memory proposal。
- 用户要求忘记时是否执行或记录处理。

## If Failed

停止写入，改为生成 proposal 或向用户确认。
