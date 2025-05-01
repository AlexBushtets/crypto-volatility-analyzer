from data_fetchers.binance_fetcher import fetch_klines
from analyzers.volatility_analyzer import calculate_volatility
from writers.csv_writer import save_to_csv
from data_fetchers.sp500_fetcher import fetch_sp500_data
import pandas as pd

# Главная функция для запуска анализа волатильности
# Вызывается как из web-интерфейса, так и вручную

def run_volatility_analysis(days_to_analyze):
    symbols = ["BTCUSDT", "ETHUSDT"]  # Криптовалюты для анализа
    all_results = []  # Сюда будем собирать результат по каждой монете

    for coin in symbols:
        print(f"Обрабатываем {coin}...")
        klines = fetch_klines(coin, interval="1d", limit=1000)
        print(f"Получено {len(klines)} свечей для {coin}")

        # Вызываем наш анализатор волатильности
        result = calculate_volatility(klines, coin, days=days_to_analyze)
        if result:
            all_results.append(result)

    if all_results:
        save_to_csv(all_results)  # Сохраняем результат криптовалют в CSV

    # --- Обработка индекса S&P500 ---
    print("\nОбрабатываем индекс S&P 500...")
    sp500_df = fetch_sp500_data(period="90d", interval="1d")
    result_sp500 = None

    if sp500_df is not None:
        # Преобразуем DataFrame в нужный формат (список списков)
        sp500_klines = sp500_df[["open_time", "high", "low"]].values.tolist()

        # Переводим дату в миллисекунды
        for row in sp500_klines:
            row[0] = int(pd.to_datetime(row[0]).timestamp() * 1000)

        # Создаём структуру в формате Binance (12 колонок)
        sp500_binance_format = []
        for row in sp500_klines:
            sp500_binance_format.append([
                row[0], 0, row[1], row[2], 0, 0, 0, 0, 0, 0, 0, 0
            ])

        # Анализируем волатильность по S&P 500
        result_sp500 = calculate_volatility(sp500_binance_format, "S&P500", days=days_to_analyze)

        if result_sp500:
            save_to_csv([result_sp500], filename="sp500_volatility.csv")

    # Возвращаем оба результата (для FastAPI)
    return all_results, result_sp500










