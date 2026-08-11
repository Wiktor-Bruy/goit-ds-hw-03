from pymongo import MongoClient
from pymongo.server_api import ServerApi

comands = ['"help" - виводить список доступних команд',
           '"cats" - виводить інформацію про всіх котів',
           '"cat [name]" - виводить інформацію про кота за іменем.',
           '"age [name] [age]" - оновлює вік коту за іменем.',
           '"features [name] [feature]" - додає характеристику до кота за іменем.',
           '"delete [name]" - видаляє кота з бази за іменем.',
           '"delete_all" - видаляє всіх котів з бази.',
           '"exit" - команда виходу з додатку.'
           'В представлених командах додаткові аргументи слід вводити без дужок - []']

mongo_url = ""

db = None
client = None

# Оскільки в url підключення до MongoDB міститься пароль, він завантажується з файлу і не буде доданий до GitHub
def load_url():
    global mongo_url
    try:
        with open("mongo.txt", "r") as file:
            mongo_url = file.read()
            return "\nUrl для підключення успішно завантажено."
    except Exception as e:
        mess = "\nФункціонал додатка буде обмежено."
        mess2 =  f"\nНе вдалось завантажити url для підключення до бази.\nПомилка: {e}"
        return mess2 + mess

# Функція підключення до зовнішньої бази даних
def connenct_to_db():
    global db
    global client
    try:
        client = MongoClient(mongo_url, server_api=ServerApi('1'))
        db = client.python
        return "\nПідключення до бази успішне."
    except Exception as e:
        return f"\nПіключення до бази провалено.\nПричина: {e}\nФункціонал додатка буде обмежений."

# Фунція парсингу команд користувача
def parse_comand(user_input: str):
    if not user_input:
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args

# Виводить інформацію про всіх котів
def show_cats():
    cats = ""
    try:
        res = db.cats.find({})
        res_arr = []
        for i in res:
            res_arr.append(i)
        if len(res_arr) == 0:
            return "\nКотиків не знайдено."
        for cat in res_arr:
            cats = cats + f"\nІм'я: {cat["name"]}, Вік: {cat["age"]}, Характеристики: {", ".join(cat["features"])}"
        return cats
    except Exception as e:
        return f"Сталась помилка при завантаженні даних: {e}"

# Виводить інформацію про кота по імені
def show_cat(args: list):
    if len(args) != 1:
        return "\nНевірно вказані параметри команди. Спробуйте заново."
    name = args[0]
    try:
        cat = db.cats.find_one({"name": name})
        if not cat:
            return "\nКота з таким ім'ям не знайдено."
        res = f"\nІм'я: {cat["name"]}, Вік: {cat["age"]}, Характеристики: {", ".join(cat["features"])}"
        return res
    except Exception as e:
        return f"Сталась помилка при завантаженні даних: {e}"

# Функція оновлення віку кота за ім'ям
def update_age(args: list):
    if len(args) != 2:
        return "\nНевірно вказані параметри команди. Спробуйте заново."
    name = args[0]
    age = args[1]
    if not age.isdecimal():
        return"\nНевірно вказані параметри команди. Вік має бути цифрою."
    try:
        res = db.cats.update_one({"name": name}, {"$set": {"age": int(age)}})
        if not res.raw_result["updatedExisting"]:
            return "\nОперація провалена, кота з таким ім'ям нема в базі."
        cat = db.cats.find_one({"name": name})
        return f"\nІм'я: {cat["name"]}, Вік: {cat["age"]}, Характеристики: {", ".join(cat["features"])}"
    except Exception as e:
        return f"Сталась помилка при оновленні даних: {e}"

# Функція додавання характеристики до кота за ім'ям
def update_features(args: list):
    if len(args) != 2:
        return "\nНевірно вказані параметри команди. Спробуйте заново."
    name = args[0]
    feat = args[1]
    try:
        res = db.cats.update_one({"name": name}, {"$push": {"features": feat}})
        if not res.raw_result["updatedExisting"]:
            return "\nОперація провалена, кота з таким ім'ям нема в базі."
        cat = db.cats.find_one({"name": name})
        return f"\nІм'я: {cat["name"]}, Вік: {cat["age"]}, Характеристики: {", ".join(cat["features"])}"
    except Exception as e:
        return f"Сталась помилка при оновленні даних: {e}"

# Функція видалення кота за ім'ям
def delete_cat(args: list):
    if len(args) != 1:
        return "\nНевірно вказані параметри команди. Спробуйте заново."
    name = args[0]
    try:
        res = db.cats.delete_one({"name": name})
        if res.deleted_count == 0:
            return "\nОперація провалена, кота з таким ім'ям нема в базі."
        return f"\nКота з ім'ям {name} видалено."
    except Exception as e:
        return f"Сталась помилка при оновленні даних: {e}"

# Функція видалення всіх 
def delete_all():
    try:
        db.cats.delete_many({})
        return f"\nВсіх котів видалено."
    except Exception as e:
        return f"Сталась помилка при оновленні даних: {e}"

# Основний процес додатка
def main():
    print("\nВітаємо в терміналі взаємодії з базою даних котиків.")
    print("\nЗавантаження url бази даних....")
    print(load_url())
    print("\nПідключення до віддаленої бази даних....")
    print(connenct_to_db())
    print("Для перегляду доступних команд введіть - help.")
    while True:
        user_comand = input("\nВеедіть бажану команду: ")
        cmd, args = parse_comand(user_comand)

        if cmd == 'help':
            for com in comands:
                print("\nДоступні команди:")
                print(com)
        elif cmd == "cats":
            print(show_cats())
        elif cmd == "cat":
            print(show_cat(args))
        elif cmd == "age":
            print(update_age(args))
        elif cmd == "features":
            print(update_features(args))
        elif cmd == "delete":
            print(delete_cat(args))
        elif cmd == "delete_all":
            print(delete_all())
        elif cmd == "exit":
            client.close()
            print("\nДякуємо за використання нашого додатку. Допобачення!")
            break
        else:
            print("\nВведена вами команда не підтримується. Можливо ви помилилися.")
            print('Команда - "help" виведе список доступних команд в додатку.')

if __name__ == "__main__":
    main()