# Дипломный проект профессии «Python-разработчик: расширенный курс»

## Backend-приложение для автоматизации закупок

### Установка и запуск проекта
<ul>
<li>pip install -r requirements.txt</li>
<li>python manage.py makemigrations</li>
<li>python manage.py migrate</li>
<li>python manage.py createsuperuser</li>
<li>python manage.py runserver</li>
</ul>
Проект будет доступен:

http://127.0.0.1:8000/

Административная панель:

http://127.0.0.1:8000/admin/

Email уведомления

Для тестирования используется вывод email в консоль.

settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

### Описание работы API

После оформления заказа письма будут отображаться в терминале.

Импорт файла с товарами реализован через метод POST http://127.0.0.1:8000/import/

#### Регистрация пользователя
Endpoint
POST /register/
Body
{
  "email": "user@mail.com",
  "password": "123456",
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "middle_name": "Ivanovich"
}
Ответ

{
  "id": 1,
  "email": "user@mail.com"
}

#### Авторизация
Endpoint
POST /login/
Body
{
  "email": "user@mail.com",
  "password": "123456"
}
Ответ
{
  "status": "logged in"
}


#### Адреса пользователя
##### Получение адресов
Endpoint
GET /addresses/
Описание
Возвращает только адреса текущего пользователя.

##### Создание адреса для отправки товара пользователю.
Endpoint
POST /addresses/
Body
{
  "city": "Moscow",
  "street": "Lenina",
  "house": "10",
  "building": "1",
  "structure": "2",
  "apartment": "15"
}


#### Товары
##### Получение списка товаров
Endpoint
GET /products/
Ответ
[
  {
    "id": 1,
    "product": {
      "id": 1,
      "name": "iPhone 15",
      "description": "Apple smartphone"
    },
    "supplier": "Apple Store",
    "price": "100000.00",
    "quantity": 5
  }
]

#### Корзина
##### Получение корзины
Endpoint
GET /basket/
Описание
Возвращает корзину текущего пользователя.

##### Добавление товара в корзину
Endpoint
POST /basket/add/
Body
{
  "product_info_id": 1,
  "quantity": 2
}
Ответ
{
  "status": "added"
}

##### Удаление товара из корзины
Endpoint
POST /basket/remove/
Body
{
  "item_id": 1
}

#### Подтверждение заказа
Endpoint
POST /order/confirm/
Body
{
  "address_id": 1
}
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
Endpoint
GET /orders/

Пользователь видит только свои заказы.

##### Получение конкретного заказа
Endpoint
GET /orders/<id>/

Возвращает подробную информацию о заказе.


