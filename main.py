from data_fetchers.binance_fetcher import fetch_klines
from analyzers.volatility_analyzer import calculate_volatility
from writers.csv_writer import save_to_csv
from tabulate import tabulate
from data_fetchers.sp500_fetcher import fetch_sp500_data
import pandas as pd

print("Старт программы...")
# Запрашиваем у пользователя количество дней
while True:
    try:
        days_to_analyze = int(input("Введите количество будних дней для расчёта волатильности (5, 10 или 30): "))
        if days_to_analyze in [5, 10, 30]:
            break
        else:
            print("Пожалуйста, введите 5, 10 или 30.")
    except ValueError:
        print("Ошибка: нужно ввести число.")


symbols = ["BTCUSDT", "ETHUSDT"]
all_results = []

for coin in symbols:
    print(f"Обрабатываем {coin}...")
    klines = fetch_klines(coin, interval="1d", limit=1000)
    print(f"Получено {len(klines)} свечей для {coin}")
    
    result = calculate_volatility(klines, coin, days=days_to_analyze)
    if result:
        all_results.append(result)

if all_results:
    print("\nИтоговая таблица средней волатильности:\n")
    from tabulate import tabulate
    print(tabulate(all_results, headers="keys", tablefmt="pretty"))
    save_to_csv(all_results)
else:
    print("Нет данных для записи.")


# === ОБРАБОТКА S&P 500 ===
print("\nОбрабатываем индекс S&P 500...")

# Загружаем данные по индексу
sp500_df = fetch_sp500_data(period="90d", interval="1d")

if sp500_df is not None:
    # Превращаем DataFrame в список списков
    sp500_klines = sp500_df[["open_time", "high", "low"]].values.tolist()

    # Переводим open_time обратно в миллисекунды для совместимости
    for row in sp500_klines:
        row[0] = int(pd.to_datetime(row[0]).timestamp() * 1000)

    # Преобразуем sp500_klines в формат Binance (добавляем пустые столбцы)
    sp500_binance_format = []
    for row in sp500_klines:
        sp500_binance_format.append([
            row[0], 0, row[1], row[2], 0, 0, 0, 0, 0, 0, 0, 0
        ])

    # Только после подготовки всех строк вызываем анализ
    result_sp500 = calculate_volatility(sp500_binance_format, "S&P500", days=days_to_analyze)

    if result_sp500:
        print("\nИтоговая таблица волатильности индекса S&P 500:\n")
        print(tabulate([result_sp500], headers="keys", tablefmt="pretty"))
        save_to_csv([result_sp500], filename="sp500_volatility.csv")
else:
    print("Не удалось получить данные по индексу S&P 500.")






