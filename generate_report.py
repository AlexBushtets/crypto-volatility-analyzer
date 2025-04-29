import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tabulate import tabulate

# Загружаем данные
btc = pd.read_csv("BTCUSDT_volatility.csv")
eth = pd.read_csv("ETHUSDT_volatility.csv")
sp500 = pd.read_csv("S&P500_volatility.csv")

# Ограничиваем по минимальной длине
min_len = min(len(btc), len(eth), len(sp500))
btc = btc.tail(min_len)
eth = eth.tail(min_len)
sp500 = sp500.tail(min_len)

# Строим график
plt.figure(figsize=(10, 6))
plt.plot(btc["date"], btc["percent_change"], label="BTCUSDT")
plt.plot(eth["date"], eth["percent_change"], label="ETHUSDT")
plt.plot(sp500["date"], sp500["percent_change"], label="S&P500")
plt.title("Сравнение волатильности за последние дни")
plt.xlabel("Дата")
plt.ylabel("Изменение (%)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Сохраняем в PDF
with PdfPages("crypto_volatility_report.pdf") as pdf:
    # Добавляем страницу с графиком
    pdf.savefig()
    plt.close()

    # Создаём страницу с таблицей (текстом)
    from matplotlib.figure import Figure
    fig = Figure(figsize=(8.5, 11))
    ax = fig.add_subplot(111)
    ax.axis("off")

    # Готовим таблицу как текст
    summary_data = [
        ["Symbol", "Average Volatility (%)"],
        ["BTCUSDT", round(btc["percent_change"].mean(), 2)],
        ["ETHUSDT", round(eth["percent_change"].mean(), 2)],
        ["S&P500", round(sp500["percent_change"].mean(), 2)]
    ]

    table_text = tabulate(summary_data, headers="firstrow", tablefmt="grid")
    ax.text(0, 1, "Таблица средней волатильности\n\n" + table_text,
            fontsize=10, fontfamily="monospace", va="top")

    pdf.savefig(fig)

print("PDF-отчёт успешно создан: crypto_volatility_report.pdf")
