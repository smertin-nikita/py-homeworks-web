# Домашнее задание к лекции «Flask»

## Задание 1

Вам нужно написать REST API (backend) для сайта объявлений.

Должны быть реализованы методы создания/удаления/редактирования объявления.    

У объявления должны быть следующие поля: 
- заголовок
- описание
- дата создания
- владелец

Результатом работы является API, написанное на Flask.

Этапы выполнения задания:

1. Сделайте роут на Flask.
2. POST метод должен создавать объявление, GET - получать объявление, DELETE - удалять объявление.

## Задание 2 *(не обязательное)

Добавить систему прав.

Создавать объявление может только авторизованный пользователь.
Удалять/редактировать может только владелец объявления.
В таблице с пользователями должны быть как минимум следующие поля: идентификатор, почта и хэш пароля.


## Команды для докера

Создаем образ для flask приложения

```bash
docker build --tag my-flask .
```

Создаем контейнер и прокидываем в него том с кодом и переменные окружения для подключения к бд. Также подключаем к сети:

```bash
docker run --name flask-test -p 5000:5000 -v C:\Users\Nikita\PycharmProjects\py-homeworks-web\flask\app:/app -e USER_DB=admin -e NAME_DB=advertisement_db -e PASSWORD_DB=admin --network my-net my-flask
```

Создаем контейнер для postgres

```bash
docker run -it -p 5431:5432 --name postgres-test -e POSTGRES_PASSWORD=password --network my-net postgres

```

Заходим в postgres

```bash
psql -U postgres -h localhost -p 5431 postgres
```

Создаем пользователя admin

```sql
create user admin with password 'admin';
```

Даем ему права на создание бд

```sql
alter role admin createrole createdb;
```

Заходим в postgres через admin

```bash
psql -U admin -h localhost -p 5431 postgres
```

Создаем бд

```sql
create database advertisement_db;
```

Выполняем команду пинг:

```bash
docker exec flask-test ping postgres-test
```

~~Для миграции бд выполнить команду:~~
```
alembic upgrade head
```
