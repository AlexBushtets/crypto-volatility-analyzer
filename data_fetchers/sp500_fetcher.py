import yfinance as yf
import pandas as pd

def fetch_sp500_data(period="90d", interval="1d"):
    """
    Загружает исторические данные для индекса S&P 500.
    
    period: за какой период загрузить данные (например, "90d" = 90 дней)
    interval: интервал свечей (например, "1d" = 1 день)
    
    Возвращает DataFrame с колонками: open_time, high, low
    """

    # Загружаем данные по тикеру ^GSPC
    sp500 = yf.download("^GSPC", period=period, interval=interval, progress=False)

    if sp500.empty:
        print("Ошибка: не удалось загрузить данные по S&P 500.")
        return None

    # Переименовываем колонки под наш стандарт
    df = pd.DataFrame({
    "open_time": sp500.index,
    "high": sp500["High"].values.flatten(),
    "low": sp500["Low"].values.flatten()
    })


    return df
