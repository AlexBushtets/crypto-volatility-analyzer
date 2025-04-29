import requests

def get_json(url, params=None):
    """
    Отправляет GET-запрос по указанному URL и возвращает ответ в формате JSON.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
