import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# Функція для обчислення віку
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
                gender = row[3]
                birth_date = datetime.strptime(row[4], '%Y-%m-%d')
                age = calculate_age(birth_date)
                data.append([gender, age])
        print("Ok")
        return data
    except Exception as e:
        print(f"Помилка при відкритті або читанні CSV-файлу: {e}")
        return None

# Функція для побудови діаграми
def plot_pie_chart(data, labels, title):
    if sum(data) == 0:  # Перевіряємо, чи всі значення рівні нулю
        print(f"Неможливо побудувати діаграму для '{title}', всі значення рівні 0.")
        return

    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    plt.title(title)
    plt.axis('equal')  # Забезпечити круглу форму
    plt.show()


# Функція для побудови стовпчикової діаграми
def plot_bar_chart(data, labels, title):
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data, color=['#ff9999','#66b3ff'])
    plt.title(title)
    plt.ylabel('Кількість')
    plt.show()

# Функція для підрахунку співробітників за статтю
def count_by_gender(data):
    gender_counter = Counter([row[0] for row in data])
    print(f"Чоловіки: {gender_counter['чоловік']}, Жінки: {gender_counter['жінка']}")
    
    # Перевірка і побудова діаграми
    plot_pie_chart([gender_counter['чоловік'], gender_counter['жінка']], ['Чоловіки', 'Жінки'], 'Розподіл за статтю')

# Функція для підрахунку співробітників за віковими категоріями
def count_by_age_category(data):
    age_categories = {'younger_18': 0, '18-45': 0, '45-70': 0, 'older_70': 0}
    
    for _, age in data:
        if age < 18:
            age_categories['younger_18'] += 1
        elif 18 <= age <= 45:
            age_categories['18-45'] += 1
        elif 46 <= age <= 70:
            age_categories['45-70'] += 1
        else:
            age_categories['older_70'] += 1
    
    print(f"Молодше 18: {age_categories['younger_18']}")
    print(f"18-45 років: {age_categories['18-45']}")
    print(f"45-70 років: {age_categories['45-70']}")
    print(f"Старше 70: {age_categories['older_70']}")
    
    # Побудова діаграми
    plot_bar_chart(list(age_categories.values()), list(age_categories.keys()), 'Розподіл за віковими категоріями')

# Функція для підрахунку співробітників за віковими категоріями та статтю
def count_by_gender_and_age_category(data):
    gender_age_categories = defaultdict(lambda: {'чоловік': 0, 'жінка': 0})
    
    for gender, age in data:
        if age < 18:
            gender_age_categories['younger_18'][gender] += 1
        elif 18 <= age <= 45:
            gender_age_categories['18-45'][gender] += 1
        elif 46 <= age <= 70:
            gender_age_categories['45-70'][gender] += 1
        else:
            gender_age_categories['older_70'][gender] += 1

    for category in gender_age_categories:
        print(f"{category}: Чоловіки: {gender_age_categories[category]['чоловік']}, Жінки: {gender_age_categories[category]['жінка']}")
        # Побудова діаграми для кожної категорії
        plot_pie_chart(
            [gender_age_categories[category]['чоловік'], gender_age_categories[category]['жінка']],
            ['Чоловіки', 'Жінки'],
            f'Розподіл за статтю у категорії {category}'
        )

# Основна функція
def main():
    csv_file = 'employees.csv'
    data = load_data_from_csv(csv_file)

    if data:
        count_by_gender(data)
        count_by_age_category(data)
        count_by_gender_and_age_category(data)

# Запуск програми
if __name__ == "__main__":
    main()
