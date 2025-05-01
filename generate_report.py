import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import json

# 📊 Подготовка данных для интерактивного графика (Plotly)
def get_plot_data():
    try:
        btc_df = pd.read_csv("BTCUSDT_volatility.csv")
        eth_df = pd.read_csv("ETHUSDT_volatility.csv")
        sp_df = pd.read_csv("S&P500_volatility.csv")
    except FileNotFoundError as e:
        print(f"❌ Не найден файл: {e.filename}")
        return None

    # 🧩 Оставляем только общие даты (чтобы графики совпадали)
    common_dates = set(btc_df["date"]) & set(eth_df["date"]) & set(sp_df["date"])
    btc_df = btc_df[btc_df["date"].isin(common_dates)].copy()
    eth_df = eth_df[eth_df["date"].isin(common_dates)].copy()
    sp_df  = sp_df[sp_df["date"].isin(common_dates)].copy()

    # ⏳ Сортировка по дате
    for df in [btc_df, eth_df, sp_df]:
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values("date", inplace=True)

    # 📤 Возвращаем данные в формате Plotly
    return json.dumps([
        {
            "x": btc_df["date"].dt.strftime("%Y-%m-%d").tolist(),
            "y": btc_df["percent_change"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "BTCUSDT"
        },
        {
            "x": eth_df["date"].dt.strftime("%Y-%m-%d").tolist(),
            "y": eth_df["percent_change"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "ETHUSDT"
        },
        {
            "x": sp_df["date"].dt.strftime("%Y-%m-%d").tolist(),
            "y": sp_df["percent_change"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "S&P500"
        }
    ])

# 📄 Генерация PDF отчёта
def generate_pdf_report():
    try:
        btc_df = pd.read_csv("BTCUSDT_volatility.csv")
        eth_df = pd.read_csv("ETHUSDT_volatility.csv")
        sp_df = pd.read_csv("S&P500_volatility.csv")
    except FileNotFoundError as e:
        print(f"❌ Ошибка: файл не найден — {e.filename}")
        return

    # 📅 Оставляем только общие даты
    common_dates = set(btc_df["date"]) & set(eth_df["date"]) & set(sp_df["date"])
    btc_df = btc_df[btc_df["date"].isin(common_dates)].copy()
    eth_df = eth_df[eth_df["date"].isin(common_dates)].copy()
    sp_df  = sp_df[sp_df["date"].isin(common_dates)].copy()

    # ⏳ Сортируем по дате
    for df in [btc_df, eth_df, sp_df]:
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values("date", inplace=True)

    # 🖨️ Рисуем и сохраняем в PDF
    with PdfPages("crypto_volatility_report.pdf") as pdf:
        plt.figure(figsize=(12, 6))

        plt.plot(btc_df["date"], btc_df["percent_change"], label="BTCUSDT", marker="o")
        plt.plot(eth_df["date"], eth_df["percent_change"], label="ETHUSDT", marker="o")
        plt.plot(sp_df["date"],  sp_df["percent_change"],  label="S&P500",  marker="o")

        plt.xlabel("Дата")
        plt.ylabel("Изменение (%)")
        plt.title("📊 Динамика дневной волатильности")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()

        pdf.savefig()
        plt.close()

    print("✅ PDF-отчёт успешно создан: crypto_volatility_report.pdf")






