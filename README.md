# HardQode Test Task
<details>
<summary>Project stack</summary>

- Python 3.11
- Django 4.2
- DRF 3.14
- drf-yasg

</details>

## Описание

Проект представляет собой веб-приложение для просмотра информации по программам онлайн-курса. 

## Установка
Клонируйте репозиторий:
```bash
git clone git@github.com:ThatCoderMan/hardqode_test_task.git
```
Активируйте вертуальное окружение:
- для Linux/MacOS
  ```bash
  python -m venv myenv
  source venv/bin/activate
  ```
- для Windows
  ```bash
  python -m venv myenv
  venv\Scripts\activate
  ```

Установите зависимости, указанные в файле `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Использование

Для запуска программы необходимо выполнить команду:
```bash
python app/manage.py runserver
```

Сайт будет доступен по адресу `127.0.0.1:8000`

> redoc `http://127.0.0.1:8000/redoc`

> swagger `http://127.0.0.1:8000/swagger`

> api `http://127.0.0.1:8000/api`

## Примеры запросов:

### Список уроков по всем продуктам пользователя:
> http://127.0.0.1:8000/api/lessons/{user}/
```json
[
  {
    "product": "string",
    "lessons": [
      {
        "lesson": "string",
        "status": "string",
        "viewed_seconds": 0
      }
    ]
  }
]
```

### Список уроков по продукту пользователя:
> http://127.0.0.1:8000/api/lessons/{user}/{product}
```json
[
  {
    "lesson": "string",
    "status": "string",
    "viewed_seconds": 0,
    "last_view": "2019-08-24"
  }
]
```

### Статистика:
> http://127.0.0.1:8000/api/statistics/
```json
[
  {
    "name": "string",
    "lessons_viewed": 0,
    "total_viewed_time": 0,
    "total_students": 0,
    "acquisition_percentage": 0
  }
]
```

### Автор проекта:

[Artemii Berezin](https://github.com/ThatCoderMan)

