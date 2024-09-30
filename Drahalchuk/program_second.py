import csv
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException

# Функція для обчислення віку на поточну дату
def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Функція для завантаження даних з CSV-файлу
def load_data_from_csv(file_name):
    if not os.path.exists(file_name):
        print("Помилка: Файл CSV не знайдено.")
        return None
    
    data = []
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаємо заголовок
            for row in reader:
                last_name = row[0]
                first_name = row[1]
                middle_name = row[2]
                birth_date = datetime.strptime(row[4], '%Y-%m-%d')
                age = calculate_age(birth_date)
                data.append([last_name, first_name + middle_name, birth_date.strftime('%Y-%m-%d'), age])
        return data
    except Exception as e:
        print(f"Помилка при відкритті або читанні CSV-файлу: {e}")
        return None

# Функція для створення XLSX-файлу
def create_xlsx(data):
    try:
        wb = Workbook()
        
        # Аркуш "all"
        ws_all = wb.active
        ws_all.title = "all"
        ws_all.append(["№", "Прізвище", "Ім’яПо батькові", "Дата народження", "Вік"])
        for idx, row in enumerate(data, 1):
            ws_all.append([idx] + row)
        
        # Створення аркушів для вікових категорій
        def filter_and_add_sheet(sheet_name, min_age, max_age=None):
            ws = wb.create_sheet(sheet_name)
            ws.append(["№", "Прізвище", "Ім’яПо батькові", "Дата народження", "Вік"])
            filtered_data = [row for row in data if row[3] >= min_age and (max_age is None or row[3] <= max_age)]
            for idx, row in enumerate(filtered_data, 1):
                ws.append([idx] + row)
        
        # Додавання аркушів із фільтрацією за віком
        filter_and_add_sheet("younger_18", 0, 17)
        filter_and_add_sheet("18-45", 18, 45)
        filter_and_add_sheet("45-70", 46, 70)
        filter_and_add_sheet("older_70", 71)

        # Збереження XLSX-файлу
        wb.save('employees.xlsx')
        print("Ok")
        
    except InvalidFileException:
        print("Помилка: Неможливо створити XLSX-файл.")
    except Exception as e:
        print(f"Сталася помилка при створенні XLSX-файлу: {e}")

# Основна функція
def main():
    csv_file = 'employees.csv'
    data = load_data_from_csv(csv_file)
    
    if data:
        create_xlsx(data)
    else:
        print("Помилка: Дані з CSV-файлу не завантажені.")

# Запуск програми
if __name__ == "__main__":
    main()
