# Дипломный проект профессии «Python-разработчик: расширенный курс»

## Backend-приложение для автоматизации закупок

### Установка и запуск проекта
<ul>
<li>Клонировать репозиторий https://github.com/Ivanchishin/dilpomnetology.git</li>
<li>Создать файл .env по примеру в проекте</li>
<li>Создать docker образ docker compose build --no-cache</li>
<li>Запустить контейнеры docker compose up -d</li>
<li>Проверить состояние docker compose ps</li>
<li>Выполнить миграции docker compose exec web python manage.py migrate</li>
<li>Создать суперпользователя docker compose exec web python manage.py createsuperuser</li>
<li>Собрать статические файлы docker compose exec web python manage.py collectstatic --noinput</li>
</ul>
Проект будет доступен:

http://127.0.0.1:8000/

Административная панель:

http://127.0.0.1:8000/admin/


### Описание работы API

После оформления заказа письма будут отображаться в терминале.

Импорт файла с товарами реализован через метод POST http://127.0.0.1:8000/import/

#### Регистрация пользователя
Endpoint<br>
POST /register/<br>
Body<br>
{<br>
  "email": "user@mail.com",<br>
  "password": "123456",<br>
  "first_name": "Ivan",<br>
  "last_name": "Ivanov",<br>
  "middle_name": "Ivanovich"<br>
}<br>
Ответ<br>
<br>
{<br>
  "id": 1,<br>
  "email": "user@mail.com"<br>
}<br>

#### Авторизация
Endpoint<br>
POST /login/<br>
Body<br>
{<br>
  "email": "user@mail.com",<br>
  "password": "123456"<br>
}<br>
Ответ
{<br>
  "status": "logged in"<br>
}<br>


#### Адреса пользователя
##### Получение адресов
Endpoint<br>
GET /addresses/<br>

Возвращает только адреса текущего пользователя.<br>

##### Создание адреса для отправки товара пользователю.
Endpoint<br>
POST /addresses/<br>
Body<br>
{<br>
  "city": "Moscow",<br>
  "street": "Lenina",<br>
  "house": "10",<br>
  "building": "1",<br>
  "structure": "2",<br>
  "apartment": "15"<br>
}<br>


#### Товары
##### Получение списка товаров
Endpoint<br>
GET /products/<br>
Ответ<br>
[<br>
  {<br>
    "id": 1,<br>
    "product": {<br>
      "id": 1,<br>
      "name": "iPhone 15",<br>
      "description": "Apple smartphone"<br>
    },<br>
    "supplier": "Apple Store",<br>
    "price": "100000.00",<br>
    "quantity": 5<br>
  }<br>
]<br>

#### Корзина
##### Получение корзины
Endpoint<br>
GET /basket/<br>

Возвращает корзину текущего пользователя.

##### Добавление товара в корзину
Endpoint<br>
POST /basket/add/<br>
Body<br>
{<br>
  "product_info_id": 1,<br>
  "quantity": 2<br>
}<br>
Ответ<br>
{<br>
  "status": "added"<br>
}<br>

##### Удаление товара из корзины
Endpoint<br>
POST /basket/remove/<br>
Body<br>
{<br>
  "item_id": 1<br>
}<br>

#### Подтверждение заказа
Endpoint<br>
POST /order/confirm/<br>
Body<br>
{<br>
  "address_id": 1<br>
}<br>
Логика действия подтверждения заказа.
<ul>
<li>создаётся заказ </li>
<li>корзина копируется в заказ </li>
<li>отправляется email клиенту </li>
<li>отправляется email администратору </li>
<li>корзина очищается </li>
</ul>

#### Заказы
##### Получение списка заказов
Endpoint<br>
GET /orders/<br>

Пользователь видит только свои заказы.

##### Получение конкретного заказа
Endpoint<br>
GET /orders/<id>/

Возвращает подробную информацию о заказе.


