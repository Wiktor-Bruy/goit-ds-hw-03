import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Глобальні змінні для роботи скрипта
mongo_url = ""
db = None
client = None

authors = []
quotes = []

page = 1
has_next_page = True
url_quotes = f"https://quotes.toscrape.com/page/"

author = ""
authors_done = []
url_author = f"https://quotes.toscrape.com"

# Оскільки в url підключення до MongoDB міститься пароль, він завантажується з файлу і не буде доданий до GitHub
def load_url():
    global mongo_url
    try:
        with open("mongo.txt", "r") as file:
            mongo_url = file.read()
            return True
    except:
        return False

# Функція підключення до зовнішньої бази даних
def connenct_to_db():
    global db
    global client
    try:
        client = MongoClient(mongo_url, server_api=ServerApi('1'))
        db = client.python
        return True
        #return "\nПідключення до бази успішне."
    except Exception as e:
        return False
        #return f"\nПіключення до бази провалено.\nПричина: {e}\nФункціонал додатка буде обмежений."

# Функція парсингу цитат
def parse_quotes():
    global quotes
    global page
    global has_next_page
    global authors_done
    global author
    global url_quotes

    try:
        while has_next_page:
            # Отримуємо дані сторінки
            html_page = requests.get(f"{url_quotes}{page}")
            soup = BeautifulSoup(html_page.text, "html.parser")

            # Отримуємо масив цитат та проходимо по ньому
            quotes_list = soup.find_all("div", class_ = "quote")
            for q in quotes_list:
                quote_n = q.find("span", class_ = "text").get_text()[1: -1]
                author_n = q.find("small", class_ = "author").get_text()
                tag_list = q.find("div", class_ = "tags").find_all("a", class_ = "tag")
                tags = []
                for t in tag_list:
                    tags.append(t.get_text())

                # Після отримання однієї цитати додаємо її до списку
                quotes.append({"tags": tags.copy(),
                               "author": f"{author_n}",
                               "quote": f"{quote_n}"})
                print("Цитату додано до списку.")

                # Перевіряємо чи є в нашому списку автор цитати. Якщо так, переходимо до наступної
                if author_n in authors_done:
                    continue

                # Якщо автора нема в нашому списку запускаємо функцію парсингу атора і додаємо його
                author = q.find("small", class_ = "author").find_next_sibling("a")["href"]
                parse_author(author)
                authors_done.append(author_n)

            print(f"\nЦитати з сторінки {page} додано, переходимо далі...\n")

            # Після проходу по всіх цитатах сторінки, перевіряємо наявність наступної
            next_btn = soup.find("ul", class_ = "pager").find("li", class_ = "next")
            if next_btn:
                # Якщо наступна сторінка є, збільшуємо лічильник сторінок
                page += 1
            else:
                # Якщо наступної сторінки нема скидаємо лічильники і завешуємо цикл парсингу сторінок
                page = 1
                author = ""
                has_next_page = False

    except Exception as e:
        print(f"\nСталась помилка при завантаженні даних: {e}")

# Функція парсингу авторів
def parse_author(author: str):
    global authors
    global url_author

    try:
        # Отримуємо дані сторінки
        html_page = requests.get(f"{url_author}{author}")
        soup = BeautifulSoup(html_page.text, "html.parser")

        # Отримуємо дані автора
        name = soup.find("h3", class_ = "author-title").get_text()
        date = soup.find("span", class_ = "author-born-date").get_text()
        location = soup.find("span", class_ = "author-born-location").get_text()
        description = soup.find("div", class_ = "author-description").get_text()[1: -1].strip()

        # Додаємо дані автора до списку авторів
        authors.append({"fullname": f"{name}",
                        "born_date": f"{date}",
                        "born_location": f"{location}",
                        "description": f"{description}"})
        print(f"Автор {name} доданий до списку.")

    except Exception as e:
        print(f"\nСталась помилка при завантаженні даних: {e}")


# Основний процес додатка
def main():
    global has_next_page
    print("\nПривіт) Даний скрипт парсить сайт 'https://quotes.toscrape.com' та збирає з нього дані цитат та їх авторів.")

    has_next_page = True
    print("Початок парсингу сторінок...")
    parse_quotes()
    print("Парсинг сторінок закінчено. Починаємо запис даних до зовнішньої бази...")
    is_mongo_url = load_url()
    if is_mongo_url:
        print("\nUrl для підключення успішно завантажено. Підключення до бази...")
        is_connect_db = connenct_to_db()
        if is_connect_db:
            print("Підключення до бази успішне. Завантаження даних...")
            try:
                db.quotes.insert_many(quotes)
                db.authors.insert_many(authors)
                print("Дані завантажено до бази. Дякуємо за використання нашого додатку.")
                client.close()
                return
            except Exception as e:
                print(f"\nЗавантаження даних не вдалося. Помилка: {e}")
        else:
            print("Піключення до бази провалено.")
            return
    else:
        print("\nНе вдалось завантажити url для підключення до бази.")
        return
    


if __name__ == "__main__":
    main()