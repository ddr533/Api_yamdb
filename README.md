[![Linters](https://github.com/ddr533/api_yamdb/actions/workflows/linters.yml/badge.svg)](https://github.com/ddr533/api_yamdb/actions/workflows/linters.yml)
# API_YAMDB  
##### Описание проекта 
Api_yamdb - собирает отзывы пользователей на произведения.
В базе проекта хранятся данные о произведениях, категориях, жанрах,
а также отзывы на произведения и комментарии пользователей. 
##### Основные возможности:
* Пользователи могут оставлять отзывы на произведения, ставить оценки, писать
комментарии.
* Администраторы могут добавлять названия новых произведений, жанры, категории.
* Администраторы могут назначать модераторов для редактирования и удаления
отзывов и комментариев пользователей.

##### Технологии 
  
 - Python 3.9   
 - Django 3.2
 - Django rest_framework 3.12
 - Sqlite3
  
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ddr533/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Загрузить данные из *.csv файлов в базу данных:

```
python manage.py load_data User static/data/users.csv
python manage.py load_data Category static/data/category.csv
python manage.py load_data Genre static/data/genre.csv
python manage.py load_data Title static/data/titles.csv
python manage.py load_data Review static/data/review.csv
python manage.py load_data Comment static/data/comments.csv
python manage.py load_data GenreTitle static/data/genre_title.csv
```

Запустить проект:

```
python manage.py runserver
```


#### Все доступные запросы можно посмотреть по адресу: redoc/


### Примеры запросов API:
* Создание нового пользователя (на почту приходит код подтверждения):
  
  - api/v1/auth/signup/
```
    {
        "email": "string",
        "username": "string",
    }

``` 
* Получение токена для аутентификации: 

  - api/v1/auth/token/
```
    {
        "username": "string",
        "confirmation_code": "string"
    }

``` 

* Получить список всех категорий Права доступа: Доступно без токена: 

  - api/v1/categories/
  - Доступные параметры: search
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "name": "string",
          "slug": "string"
        }
      ]
    }

``` 

* Получить список всех жанров. Права доступа: Доступно без токена: 

  - api/v1/genres/
  - Доступные параметры: search
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "name": "string",
          "slug": "string"
        }
      ]
    }

``` 

* Получить список всех произведений. Права доступа: Доступно без токена: 

  - api/v1/users/me/
  - Доступные параметры: filter по полям category, genre, year, name
 
```
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

``` 
* Получить список всех отзывов. Права доступа: Доступно без токена: 

  - api/v1/titles/{title_id}/reviews/
 
```
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

``` 
* Добавить новый отзыв. Пользователь может оставить только один отзыв
на произведение. Права доступа: Аутентифицированные пользователи: 

  - api/v1/titles/{title_id}/reviews/
 
```
    {
      "text": "string",
      "score": 1
    }

``` 
* Получить список всех комментариев к отзыву по id. Права доступа: Доступно без токена: 

  - api/v1/titles/{title_id}/reviews/{review_id}/comments/
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "pub_date": "2019-08-24T14:15:22Z"
        }
      ]
    }

``` 
* Получить данные своей учетной записи: 

  - api/v1/users/me/
 
```
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }

``` 



### Авторы:
Андрей Брусилов, Андрей Дрогаль, Степан Васильев, Yandex_Practicum.
