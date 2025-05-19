
# 📊 Crypto Volatility Analyzer

Веб-приложение на Python + FastAPI для анализа волатильности криптовалют (BTC, ETH) и индекса S&P 500. Показывает среднюю и дневную волатильность за выбранный период — 5, 10, 30 или 90 дней. Строит таблицы, графики и формирует PDF-отчёт.

## 🚀 Возможности

- Анализ волатильности за 5, 10, 30 и 90 будних дней
- Расчёт волатильности на основе диапазона "максимум–минимум"
- Объединённая сводная таблица по криптовалютам и индексу S&P 500
- Ежедневные таблицы по каждой монете и по индексу
- Интерактивный график изменения в % (Plotly)
- Генерация PDF-отчёта
- Telegram-бот (в процессе подключения)

## 💾 Установка

### 1. Клонировать репозиторий:

```bash
git clone https://github.com/AlexBushtets/crypto-volatility-analyzer.git
cd crypto-volatility-analyzer
```

### 2. Создать виртуальное окружение (по желанию):

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Установить зависимости:

```bash
pip install -r requirements.txt
```

## ▶️ Запуск

Запусти сервер с помощью Uvicorn:

```bash
uvicorn webapp:app --reload
```

Открой браузер и перейди по адресу:  
http://127.0.0.1:8000

## 📋 Использование

1. Выберите нужный период анализа (5, 10, 30 или 90 дней)
2. Нажмите кнопку "Запустить анализ"
3. Посмотрите таблицы с результатами, график и ссылку для скачивания PDF

## 📦 Структура проекта

```
crypto-volatility-analyzer/
├── webapp.py
├── requirements.txt
├── templates/
├── analyzers/
├── data_fetchers/
├── writers/
├── reports/
└── static/
```

## 📄 Пример отчёта

PDF-отчёт формируется автоматически после анализа. Включает:
- таблицу средней волатильности
- таблицы ежедневных изменений
- график динамики

# 📈 Crypto Volatility Analyzer

Анализ волатильности BTC, ETH и индекса S&P500 за 5, 10, 30 и 90 дней с веб-интерфейсом, генерацией PDF-отчётов и Telegram-ботом с автоуведомлениями.

---

## 🚀 Возможности

- Анализ дневной волатильности за выбранный период
- Подсветка минимальной/максимальной волатильности в таблицах
- Генерация PDF-отчёта
- Веб-интерфейс (FastAPI + Jinja2)
- Telegram-бот:
  - /analyze_5, /analyze_10, /analyze_30, /analyze_90
  - Автоуведомления при экстремальной волатильности в 6:00 (Europe/Rome)

---

## 📌 Пороговые значения для выделения:

| Актив    | Минимум (%) | Максимум (%) |
|----------|--------------|----------------|
| BTCUSDT  | ≤ 2%         | ≥ 8%          |
| ETHUSDT  | ≤ 3%         | ≥ 15%         |

---

## 🧪 Установка

```bash
git clone https://github.com/AlexBushtets/crypto-volatility-analyzer.git
cd crypto-volatility-analyzer
python -m venv venv
venv\Scripts\activate   # или source venv/bin/activate на Linux/macOS
pip install -r requirements.txt
```

---

## ▶ Запуск локально

```bash
uvicorn webapp:app --reload
```

---

## 🌐 Развёртывание на [Render.com](https://render.com)

1. Создай новый **Web Service**
2. В настройках **Environment** добавь:
    ```
    BOT_TOKEN=твой_бот_токен
    TELEGRAM_CHAT_ID=твой_чат_ID
    ```
3. Зайди в Deploy → Manual Deploy → Deploy latest commit

---

## 📬 Telegram-бот

- `/start` — приветствие
- `/analyze_5` — анализ за 5 дней
- `/analyze_10` — анализ за 10 дней
- `/analyze_30` — анализ за 30 дней
- `/analyze_90` — анализ за 90 дней

⚠️ Бот отправит автоуведомление, если **вчерашняя волатильность была экстремальной** по BTC или ETH.

---

## 🖼 Интерфейс

- Выбор периода анализа
- Сводная таблица волатильности
- Ежедневные таблицы с подсветкой (цвета: зелёный, розовый, жёлтый)
- Скачивание PDF-отчёта
- График изменений

---

## 📄 License

MIT License.
