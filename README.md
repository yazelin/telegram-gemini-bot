# Telegram Gemini CLI Bot (FastAPI MVP)

這是一個基於 **FastAPI** 與 **python-telegram-bot** 的簡單應用程式，採用 **Polling (輪詢)** 模式運行。當 Telegram Bot 收到訊息時，會直接呼叫系統中的 `gemini -p` 指令處理訊息，並將結果推送回 Telegram。

## 🚀 特色
- **環境隔離**: 使用 `uv` 快速建立 Python 環境。
- **CLI 整合**: 直接呼叫系統已配置好的 `gemini` 指令，無需在程式碼中管理 API Key。
- **非同步執行**: 使用 `asyncio` 執行外部指令，不會阻塞服務。

---

## 📋 系統需求
在開始之前，請確保您的環境已安裝以下工具：

1. **Python 3.10+**
2. **uv**: 用於管理 Python 套件與環境。 ([安裝指南](https://github.com/astral-sh/uv))
3. **Gemini CLI**: 系統中必須可執行 `gemini` 指令（且已完成認證設定，手動執行 `gemini -p "test"` 需能正確回傳）。
4. **Telegram Bot Token**: 向 [@BotFather](https://t.me/botfather) 申請。

---

## 🛠️ 安裝與設定

### 1. 進入專案目錄
```bash
cd telegram-gemini-bot
```

### 2. 設定環境變數
編輯目錄下的 `.env` 檔案，填入您的 Telegram Token：

```bash
# 編輯 .env 檔案
TELEGRAM_BOT_TOKEN=你的_TELEGRAM_BOT_TOKEN
```

### 3. 初始化環境 (選用)
如果您是第一次啟動，可以執行以下指令讓 `uv` 自動安裝套件：
```bash
uv sync
```

---

## 🏃 啟動流程

### 方式 A：使用內建腳本 (推薦)
我們提供了一個 `run.sh` 腳本，會自動檢查環境並啟動：
```bash
# 賦予權限 (僅第一次)
chmod +x run.sh

# 啟動服務
./run.sh
```

### 方式 B：手動啟動
```bash
uv run python main.py
```

服務啟動後：
- **API 狀態**: 可存取 `http://localhost:8000/` 查看。
- **Telegram Bot**: 現在可以對您的 Bot 發送訊息。

---

## ⚙️ 環境變數說明

| 變數名稱 | 說明 | 範例 |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot 的存取金鑰 | `123456:ABC-DEF1234...` |

> **注意**: 此版本不使用 `GEMINI_API_KEY` 環境變數，因為它是透過呼叫系統指令 `gemini` 來運作的。

---

## 📝 程式邏輯說明
1. **FastAPI**: 作為主要的 Web Server，利用 `lifespan` 事件在背景啟動 Telegram Polling。
2. **Polling**: `python-telegram-bot` 會持續監聽新訊息。
3. **Gemini CLI**: 接收到訊息後，執行 `subprocess: gemini -p "<USER_MESSAGE>"`。
4. **Reply**: 讀取指令輸出的內容並透過 Telegram 回傳。

---

## ⚠️ 常見問題
- **找不到 gemini 指令**: 請確保 `gemini` 指令在您的系統 `$PATH` 中。
- **權限錯誤**: 如果 `run.sh` 無法執行，請確認權限 `chmod +x run.sh`。
- **訊息無回應**: 請檢查控制台 log，確認 `gemini` 指令是否因未授權或網路問題而失敗。
