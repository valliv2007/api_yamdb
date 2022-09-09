# Проект API YAMDB

### Описание проекта:
В проекте Yamdb можно оставить отзыв на произведения («Книги», «Фильмы», «Музыка» и пр.). Отзывы состоят из текстовой заметки и оценки от 1 до 10. Из оценок складывается рейтинг. Произведения можно отфильтровать по категориям, либо по жанру.

### Описание проекта:
Сайт Yatube - это соцсеть, где можно делать публикации на различные темы. Подписываться на авторов, а так же оставлять комментарии. Это API для сайта. 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/valliv2007/api_yamdb.git
```

```sh
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```sh
python -m venv venv
```

```sh
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Выполнить миграции:

```sh
python manage.py migrate
```

Запустить проект:

```sh
python manage.py runserver
```

### Примеры запросов API к сайту
Запрос:
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Ответ: 
```sh
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
Запрос:
```
POST http://127.0.0.1:8000/api/v1/titles/
```
```sh
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
    "string"
],
"category": "string"
}
```
Ответ: 
```sh
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
    {
        "name": "string",
        "slug": "string"
    }
],
"category": {
    "name": "string",
    "slug": "string"
    }
}
```

Запрос:
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```sh
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
Запрос: 
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```sh
{
"text": "string",
"score": 1
}
``` 

### Над проектом работали
- Снежко Илья *(Тимлид)*
- Авров Александр
- Мишанькин Алексей