# goit-ds-hw-03

This is one of the projects I worked on during my studies. It contains two scripts that perform their tasks when run.

### main.py

This script is designed to interact with a remote MongoDB database, specifically a collection of cats.
After launching, the script waits for commands from the user, which it will execute.

- Displays all data in a collection.
- Displays data for a single document by name.
- Updates data by name.
- Deletes a document by name.
- Removes all documents from a collection.

### parse.py

После запуска этот скрипт начнет парсить сайт https://quotes.toscrape.com просматривая его страницы с цытатами. Он будет собирать их в коллекцию. Также он будет собирать информацию об авторах цитат. После окончания сбора со всех страниц, он добавит эти данные во внешнюю базу MongoDB.

## Tech stack

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" alt="python" width="65"><img src="https://github.com/devicons/devicon/blob/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="65">

## How to use

1. Copy this repository.
   ```
   git clone (SSH or HTTPS key)
   ```
2. You must have a MongoDB database created on their service. There should be a python database and collections of cats, authors and quotes.
3. At the root of the project, add a mongo.txt file in which you add the connection string to the database.
4. Install project dependencies.
   ```
   poetry install
   ```
5. Run the script you need using dependencies.
   ```
   poetry run main.py
   ```
   or
   ```
   poetry run parse.py
   ```
