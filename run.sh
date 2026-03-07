#!/bin/bash

# 進入專案目錄
cd "$(dirname "$0")"

# 1. 檢查 .env 檔案是否存在
if [ ! -f .env ]; then
    echo "錯誤: 找不到 .env 檔案！請先建立並設定金鑰。"
    exit 1
fi

# 2. 檢查 Telegram Token 是否已填入
if grep -q "YOUR_TELEGRAM_BOT_TOKEN" .env; then
    echo "警告: 偵測到預設金鑰字串。請編輯 .env 檔案並填入真正的 TELEGRAM_BOT_TOKEN。"
    exit 1
fi

# 3. 檢查系統中是否有 gemini 指令
if ! command -v gemini &> /dev/null; then
    echo "錯誤: 找不到 'gemini' 指令！請確保您已安裝並設定 Gemini CLI。"
    exit 1
fi

echo "正在啟動 Telegram Gemini CLI Bot (FastAPI)..."
echo "模式：直接呼叫系統 'gemini' 指令"
echo "按 Ctrl+C 可以停止程式。"

# 使用 uv 執行程式
uv run python main.py
