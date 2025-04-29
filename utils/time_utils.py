import datetime

def is_weekday(timestamp):
    """
    Проверяет, является ли дата будним днём (Понедельник-Пятница).
    timestamp - время в формате UNIX миллисекунд.
    """
    dt = datetime.datetime.utcfromtimestamp(timestamp / 1000)
    return dt.weekday() < 5  # 0-4 это Пн-Пт

def get_last_weekdays_dates(count):
    """
    Возвращает список дат последних рабочих дней в формате 'YYYY-MM-DD'.
    """
    today = datetime.datetime.utcnow()
    dates = []
    while len(dates) < count:
        if today.weekday() < 5:
            dates.append(today.strftime('%Y-%m-%d'))
        today -= datetime.timedelta(days=1)
    return dates
