import pandas as pd

def calculate_volatility(klines, symbol, days=5):

    """
    Рассчитывает волатильность монеты за последние N будних дней.
    Сохраняет таблицу в CSV-файл.

    klines: список свечей с биржи
    symbol: строка, например "BTCUSDT"
    days: количество будних дней для анализа (по умолчанию 5)
    """

    # Превращаем список в таблицу pandas
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])

    # Преобразуем данные к числовому типу
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')

    # Убираем субботу и воскресенье
    # df = df[~df['open_time'].dt.dayofweek.isin([5, 6])]

    # Берём нужное количество последних будних дней
    last_n = df.tail(days)

    # Если не хватает данных — предупреждаем
    if len(last_n) < days:
        print(f"Недостаточно данных для {symbol}, доступно только {len(last_n)} будних дней.")
        return None

    result_rows = []
    total_points = 0
    total_percent = 0

    # Обрабатываем каждый день отдельно
    for index, row in last_n.iterrows():
        high = row["high"]
        low = row["low"]

        # Разница между максимумом и минимумом (в пунктах)
        points = round(high - low)

        # Процент изменения от минимума к максимуму
        pct_change = round(((high - low) / low) * 100, 2)

        # Добавляем в общую сумму
        total_points += points
        total_percent += pct_change

        # Сохраняем строку таблицы
        result_rows.append({
            "date": row["open_time"].strftime("%Y-%m-%d"),
            "points": points,
            "percent_change": pct_change
        })

    # Считаем средние значения
    avg_points = round(total_points / days, 2)
    avg_percent = round(total_percent / days, 2)

    # Печатаем таблицу в консоль
    print(f"\nВолатильность {symbol} за последние {days} будних дней:\n")
    print("+------------+--------+------------------+")
    print("|    Дата    | Пункты | Изменение (%)    |")
    print("+------------+--------+------------------+")
    for r in result_rows:
        print(f"| {r['date']} | {str(r['points']).rjust(6)} | {str(r['percent_change']).rjust(16)} |")
    print("+------------+--------+------------------+")
    print(f"|  Средняя   | {str(avg_points).rjust(6)} | {str(avg_percent).rjust(16)} |")
    print("+------------+--------+------------------+")

    # Сохраняем в файл CSV
    df_result = pd.DataFrame(result_rows)
    filename = f"{symbol}_volatility.csv"
    df_result.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Таблица для {symbol} сохранена в файл: {filename}\n")

    # Возвращаем краткий итог
    return {
        "symbol": symbol,
        "average_volatility_points": avg_points,
        "average_volatility_percent": avg_percent,
        "daily_data": result_rows  # ← добавим подробную таблицу
    }


    


