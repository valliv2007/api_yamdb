# Проект API YAMDB
### Описание проекта:
В проекте Yamdb можно оставить отзыв на произведения ("Книги", "Фильмы", "Музыка" и пр.). Отзывы состоят из текстовой заметки и оценки от 1 до 10. Рейтинг складывается из оценок. Произведения можно отфильтровать по категориям, либо по жанру.
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
source venv/bin/activate or source venv/Scripts/activate
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
## Документация по запросам
см. yatube_api/static/redoc.yaml  или после запуска на localhost по ссылке http://127.0.0.1:8000/redoc/
### Примеры запросов API к сайту
Запрос на просмотр произведений:
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Ответ: 
```sh
{    
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Побег из Шоушенка",
            "year": 1994,
            "rating": 9,
            "description": "Фильм про побег из тюрьмы",
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        }
    ]
}
```
Запрос на получение жанров:
```
GET http://127.0.0.1:8000/api/v1/genres/
```
Ответ: 
```sh
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Драма",
            "slug": "drama"
        },
        {
            "name": "Комедия",
            "slug": "comedy"
        },
        {
            "name": "Вестерн",
            "slug": "western"
        }
    ]
}
```
Запрос на получение категорий:
```
GET http://127.0.0.1:8000/api/v1/categories/
```
Ответ: 
```sh
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Фильм",
            "slug": "movie"
        },
        {
            "name": "Книга",
            "slug": "book"
        },
        {
            "name": "Музыка",
            "slug": "music"
        }
    ]
}
```
Запрос на получение отзывов к произведению:
```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/
```
Ответ: 
```sh
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Мне понравилось",
            "author": "bingobongo",
            "score": 9,
            "pub_date": "2019-09-24T21:08:21.567000Z"
        },
        {
            "id": 2,
            "text": "Эти стены имеют одно свойство: сначала ты их ненавидишь, потом привыкаешь, а потом не можешь без них жить",
            "author": "capt_obvious",
            "score": 10,
            "pub_date": "2019-09-24T21:08:21.567000Z"
        }
    ]
}
```
Запрос на получение комментариев к отзыву:
```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/
```
Ответ: 
```sh
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "text": "Солидарен",
            "author": "anonymous",
            "pub_date": "2022-09-10T19:18:38.659928Z"
        }
    ]
}
```
Запрос регистрации нового пользователя:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```
```sh
{    
    "username": "Alex",
    "email": "myemail@mail.com"
}
```
Ответ:
```sh
{    
    "username": "Alex",
    "email": "myemail@mail.com"
}
```
Запрос на получение токена:
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```
```sh
{
    "username": "Alex",
    "confirmation_code": "642-5e3b203c6ac94a6cd822"
}
```
Ответ:
```sh
{    
    "token": "efyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzMjY5MDcwLCJpYXdvdsQiOjE2NjI4MzcwNzAsImp0aSI6IjM4M2U4MGI1NWZhODQ3ZGM4MWE2ZTM3MGI2NjdjYzBjIiwidXNlcl9pZCI6MTA2fQ.3JQxxkFOIjdISs7FgtfArdJhQ32JyIsEj6N5phzYqf0"
}
```
### Над проектом работали
- Snezhko Ilya *(Teamlead)* / GitHub: https://github.com/valliv2007
- Avrov Alexander / GitHub: https://github.com/AlexanderAvrov
- Mishankin Alexey / GitHub: https://github.com/amishankin
