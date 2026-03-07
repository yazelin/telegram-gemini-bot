import os
import asyncio
import logging
import subprocess
from fastapi import FastAPI
from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# 設定日誌
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# 呼叫 Gemini CLI 的函式
async def call_gemini_cli(prompt: str) -> str:
    try:
        # 使用 asyncio 執行外部指令: gemini -p "prompt"
        # 注意: 這裡假設環境中可以直接執行 'gemini' 指令
        process = await asyncio.create_subprocess_exec(
            "gemini", "-p", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return stdout.decode().strip()
        else:
            error_msg = stderr.decode().strip()
            logger.error(f"Gemini CLI 錯誤: {error_msg}")
            return f"Error: {error_msg}"
            
    except Exception as e:
        logger.error(f"執行 Gemini CLI 時發生異常: {e}")
        return "抱歉，系統執行指令時發生錯誤。"

# Telegram 訊息處理器
async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    logger.info(f"收到 Telegram 訊息: {user_text}")

    # 呼叫 Gemini CLI 處理訊息
    reply_text = await call_gemini_cli(user_text)
    
    # 將訊息推送回 Telegram
    if reply_text:
        await update.message.reply_text(reply_text)
    else:
        await update.message.reply_text("Gemini 沒有回傳任何內容。")

# Telegram Bot 初始化
async def run_bot_polling():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.error("請在 .env 中設定 TELEGRAM_BOT_TOKEN")
        return

    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    
    await application.initialize()
    await application.start()
    logger.info("Telegram Bot 已啟動 (透過 Gemini CLI 模式)...")
    await application.updater.start_polling()

# FastAPI 生命週期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = asyncio.create_task(run_bot_polling())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def status():
    return {"status": "online", "mode": "cli_polling"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
