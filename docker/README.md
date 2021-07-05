# Домашнее задание к лекции «Docker»

## Задание 1

По аналогии с практикой из лекции создайте свой docker image с http сервером nginx. Замените страницу приветсвия Nginx на своё (измените текст приветствия на той же странице).

<details><summary>Подсказки: </summary>  
В официальном образе nginx стандартный путь к статичным файлам `/usr/share/nginx/html`.  
</details>

На проверку присылается GitHub репозиторий с Dockerfile и статичными файлами для него.

## Команды для docker

Создие образа

```bash
docker build --tag hello-nginx .
```

Создание и запуск контейнера

```bash
docker run -d --name ngnix-test -p 5000:80 hello-nginx
```
