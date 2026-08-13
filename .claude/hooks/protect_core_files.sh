#!/usr/bin/env bash
# PreToolUse hook — 保护核心人格/记忆文件不被直接 Edit/Write
# 设置 ALLOW_CORE_EDIT=true 可豁免

set -e

TOOL_NAME="${CLAUDE_TOOL_NAME:-}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

# 只有 Edit 和 Write 需要检查
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

# 豁免
if [[ "${ALLOW_CORE_EDIT:-}" == "true" ]]; then
    exit 0
fi

# 提取 file_path（可能在嵌套 JSON 中）
FILE_PATH=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    fp = data.get('file_path', '') or data.get('path', '')
    print(fp)
except:
    print('')
" 2>/dev/null)

if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# 受保护路径模式
PROTECTED_PATTERNS=(
    "persona/SOUL.md"
    "persona/cognitive_style.md"
    "persona/emotional_map.md"
    "persona/language_fingerprint.md"
    "persona/boundaries.md"
    "persona/value_system.md"
    "persona/inner_contradictions.md"
    "memory/long_term_memory.md"
    "memory/emotional_memory.md"
    "memory/relationship_timeline.md"
    "evolution/evolution_rules.md"
    ".claude/settings.json"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "⛔ [PreToolUse Hook] 文件 '$FILE_PATH' 受核心保护。"
        echo "   直接修改此文件被阻止。请通过 evolution/proposals/ 流程提交变更。"
        echo "   如需强制修改，设置环境变量 ALLOW_CORE_EDIT=true 后重试。"
        exit 1
    fi
done

exit 0
