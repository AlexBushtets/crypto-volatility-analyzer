import csv

def save_to_csv(results, filename="volatility_results.csv"):
    if not results:
        print("Нет данных для сохранения.")
        return

    # Автоматически берём ключи из первого словаря
    fieldnames = results[0].keys()

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Данные сохранены в {filename}")



