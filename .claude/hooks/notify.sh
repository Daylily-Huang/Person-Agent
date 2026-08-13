#!/usr/bin/env bash
# Notification hook — 桌面通知
# Windows 环境使用 PowerShell 弹出通知

EVENT_TYPE="${CLAUDE_NOTIFICATION_TYPE:-}"
EVENT_MESSAGE="${CLAUDE_NOTIFICATION_MESSAGE:-}"

# 只处理权限提示和空闲提示
if [[ "$EVENT_TYPE" != "permission_prompt" && "$EVENT_TYPE" != "idle_prompt" ]]; then
    exit 0
fi

# 构造通知内容
if [[ "$EVENT_TYPE" == "permission_prompt" ]]; then
    TITLE="Claude Code — 需要确认"
    BODY="工具请求权限，请查看终端。"
elif [[ "$EVENT_TYPE" == "idle_prompt" ]]; then
    TITLE="Claude Code — 等待输入"
    BODY="Claude 空闲超过 60 秒，等待你的回复。"
fi

# Windows Toast 通知（PowerShell）
powershell.exe -NoProfile -Command "
Add-Type -AssemblyName System.Windows.Forms
\$notification = New-Object System.Windows.Forms.NotifyIcon
\$notification.Icon = [System.Drawing.SystemIcons]::Information
\$notification.BalloonTipTitle = '$TITLE'
\$notification.BalloonTipText = '$BODY'
\$notification.Visible = \$true
\$notification.ShowBalloonTip(5000)
Start-Sleep -Seconds 6
\$notification.Dispose()
" 2>/dev/null || true

exit 0
