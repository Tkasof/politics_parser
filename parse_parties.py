from bs4 import BeautifulSoup
import json
import os

# Проверяем есть ли файл с сохраненной страницей
if not os.path.exists("parties_page.html"):
    print("ОШИБКА: Файл 'parties_page.html' не найден!")
    print("Сначала сохраните страницу через браузер (Cmd+S)")
    exit()

# Читаем файл
try:
    with open("parties_page.html", "r", encoding="utf-8") as file:
        html_content = file.read()
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    exit()

# Создаем парсер
soup = BeautifulSoup(html_content, "html.parser")

# Находим раздел с партиями
parties_section = soup.find("div", id="section-765")

if not parties_section:
    print("Не найден раздел с партиями!")
    exit()

# Находим все элементы списка с партиями
party_items = parties_section.find_all("li")

# Обрабатываем каждую партию
parties_data = []

for item in party_items:
    # Находим ссылку внутри элемента
    link = item.find("a")
    
    if link:
        # Получаем название партии (текст ссылки)
        party_name = link.get_text(strip=True)
        
        # Получаем ссылку
        doc_url = link.get("href")
        
        # Если ссылка относительная, делаем абсолютной
        if doc_url and doc_url.startswith("/"):
            doc_url = "https://minjust.gov.ru" + doc_url
        
        # Добавляем в результат
        parties_data.append({
            "name": party_name,
            "doc_url": doc_url
        })

# Выводим результаты
for i, party in enumerate(parties_data, 1):
    print(f"{i}. {party['name']}")
    if party['doc_url']:
        print(f"   Документ: {party['doc_url']}")
    else:
        print(f"   Документ: нет")
    print()

# Сохраняем в JSON
try:
    with open("parties.json", "w", encoding="utf-8") as f:
        json.dump(parties_data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в 'parties.json'")
except Exception as e:
    print(f"Ошибка при сохранении: {e}")