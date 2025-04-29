from data_fetchers.binance_fetcher import fetch_klines
from analyzers.volatility_analyzer import calculate_volatility
from writers.csv_writer import save_to_csv
from tabulate import tabulate

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






