### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с переменными окружения:

```
FLASK_APP=yacut
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
FLASK_DEBUG=1
DISK_TOKEN=DISK_TOKEN
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```
