import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
btc = pd.read_csv("BTCUSDT_volatility.csv")
eth = pd.read_csv("ETHUSDT_volatility.csv")
sp500 = pd.read_csv("S&P500_volatility.csv")

# Ограничиваем до одинакового количества строк (на всякий случай)
min_len = min(len(btc), len(eth), len(sp500))
btc = btc.tail(min_len)
eth = eth.tail(min_len)
sp500 = sp500.tail(min_len)

# График
plt.figure(figsize=(10, 6))
plt.plot(btc["date"], btc["percent_change"], label="BTCUSDT")
plt.plot(eth["date"], eth["percent_change"], label="ETHUSDT")
plt.plot(sp500["date"], sp500["percent_change"], label="S&P500")

# Оформление
plt.title("Сравнение волатильности за последние дни")
plt.xlabel("Дата")
plt.ylabel("Изменение (%)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Показываем
plt.show()
