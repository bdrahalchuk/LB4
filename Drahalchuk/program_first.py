import csv
from faker import Faker # type: ignore
import random

# Ініціалізація Faker з українською локалізацією
fake = Faker('uk_UA')

# Кількість записів
total_records = 2000
female_ratio = 0.4
male_ratio = 0.6

female_count = int(total_records * female_ratio)
male_count = total_records - female_count

# Функція для генерації запису
def generate_record(gender):
    if gender == 'жінка':
        first_name = fake.first_name_female()
        middle_name = fake.middle_name_female()
    else:
        first_name = fake.first_name_male()
        middle_name = fake.middle_name_male()

    last_name = fake.last_name()
    birth_date = fake.date_of_birth(minimum_age=16, maximum_age=85).strftime('%Y-%m-%d')
    job = fake.job()
    city = fake.city()
    address = fake.address()
    phone = fake.phone_number()
    email = fake.email()

    return [last_name, first_name, middle_name, gender, birth_date, job, city, address, phone, email]

# Генерація даних
data = []
for _ in range(female_count):
    data.append(generate_record('жінка'))

for _ in range(male_count):
    data.append(generate_record('чоловік'))

# Перемішування записів
random.shuffle(data)

# Збереження в CSV-файл
with open('employees.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Заголовки таблиці
    writer.writerow(['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'])
    # Запис даних
    writer.writerows(data)

print("Файл 'employees.csv' створено з 2000 записами.")
