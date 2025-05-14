
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from analysis_core import run_volatility_analysis

# Включаем логирование (по желанию)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ваш токен от BotFather (замени ниже на свой)
BOT_TOKEN = "7412973245:AAFZPDESRY-hWFt5M0YGyxrhjNJM3rA0oQ4"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Привет! Я бот для анализа волатильности. Отправь одну из команд:
/analyze_5
/analyze_10
/analyze_30
/analyze_90"""
    )

# Универсальный обработчик анализа
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE, days: int):
    await update.message.reply_text(f"🔍 Анализирую волатильность за {days} дней...")

    crypto_results, sp500_result = run_volatility_analysis(days)

    response = f"📊 <b>Волатильность за {days} дней:</b>\n\n"

    for coin in crypto_results:
        response += f"<b>{coin['symbol']}</b> — {coin['average_volatility_points']:.1f} пунктов, {coin['average_volatility_percent']:.2f}%\n"

    response += f"<b>{sp500_result['symbol']}</b> — {sp500_result['average_volatility_points']:.1f} пунктов, {sp500_result['average_volatility_percent']:.2f}%\n"

    response += "\n📌 Вы можете выбрать:\n/analyze_5  /analyze_10  /analyze_30  /analyze_90"

    await update.message.reply_text(response, parse_mode="HTML")

# Создаём и запускаем бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    for d in [5, 10, 30, 90]:
        app.add_handler(CommandHandler(f"analyze_{d}", lambda u, c, d=d: analyze(u, c, d)))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
