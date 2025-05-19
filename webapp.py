import matplotlib
matplotlib.use("Agg")

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from analysis_core import run_volatility_analysis
from generate_report import generate_pdf_report, get_plot_data

import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Telegram Bot Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для анализа волатильности. Отправь одну из команд:\n"
        "/analyze_5\n/analyze_10\n/analyze_30\n/analyze_90"
    )

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE, days: int):
    await update.message.reply_text(f"🔍 Анализирую волатильность за {days} дней...")
    crypto_results, sp500_result = run_volatility_analysis(days)
    response = f"📊 <b>Волатильность за {days} дней:</b>\n\n"
    for coin in crypto_results:
        response += f"<b>{coin['symbol']}</b> — {coin['average_volatility_points']:.1f} пунктов, {coin['average_volatility_percent']:.2f}%\n"
    response += f"<b>{sp500_result['symbol']}</b> — {sp500_result['average_volatility_points']:.1f} пунктов, {sp500_result['average_volatility_percent']:.2f}%\n"
    response += "\n📌 Выберите период:\n/analyze_5  /analyze_10  /analyze_30  /analyze_90"
    await update.message.reply_text(response, parse_mode="HTML")

# Генератор обработчиков
def make_analyze_handler(d):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await analyze_command(update, context, d)
    return handler

# FastAPI setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(zip=zip)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    print("🔍 Загружается шаблон index.html")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, days: int = Form(...)):
    crypto_results, sp500_result = run_volatility_analysis(days)
    generate_pdf_report()
    plot_data = get_plot_data()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "days": days,
        "crypto_results": crypto_results,
        "sp500_result": sp500_result,
        "report_url": "/download/report",
        "plot_data": plot_data,
        "crypto_tables": [coin["daily_data"] for coin in crypto_results],
        "sp500_table": sp500_result["daily_data"]
    })

@app.get("/download/report")
def download_report():
    filepath = "crypto_volatility_report.pdf"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type='application/pdf', filename="volatility_report.pdf")
    return {"error": "Файл не найден"}

@app.on_event("startup")
async def start_bot():
    print("🌀 Вызван start_bot()")
    if not BOT_TOKEN:
        print("⚠️ BOT_TOKEN не задан в переменных окружения.")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))

    for d in [5, 10, 30, 90]:
        application.add_handler(CommandHandler(f"analyze_{d}", make_analyze_handler(d)))

    print("🤖 Telegram-бот запускается...")

    await application.initialize()
    await application.start()
    asyncio.create_task(application.updater.start_polling())

    print("🤖 Telegram-бот запущен.")

