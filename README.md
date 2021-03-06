## **Мини-сервис "Менеджер чеков"**
У сети ресторанов доставки "ФорФар" есть множество точек, на которых готовятся заказы для клиентов. 
Каждый клиент хочет вместе с заказом получить чек, содержащий детальную информацию о заказе. 
Сотрудники кухни также хотят чек, чтобы в процессе готовки и упаковки заказа не забыть положить всё что нужно. 
Задача помочь и тем и другим, написав сервис для генерации чеков.
### Реализованы следующие задачи:
* Сервис получает информация о новом заказе (order), и после создает в БД 2-а типа чека для конкретного магазина (point_id): клиента и кухни, и конвертирует в pdf-файлы. 
* По соответствующему принтеру (api_key) вы можете запросить список чеков (id), которые уже сгенерированы для конкретного принтера. 
* А также по соответствующему принтеру (api_key) и чеку (check_id) вы можете получить pdf-файл чека на печать.

### Инструменты разработки:

**Стек:**

* Django 3.2.11
* DRF 3.13.1
* PostgreSQL 9.6 (через сервис docker-compose)
* Django-rq (асинхронный worker)
* Redis (через сервис docker-compose)
* wkhtmltopdf (через сервис docker-compose)

Подгрузите все зависимости в проект, введите в терминале: "pip install -r requirements.txt" либо установите каждый пакет отдельно.

Для запуска сервисов необходимо установить **docker, docker-compose**

После запустите:
* docker-compose up (установка и запуск сервисов)
* python manage.py makemigrations
* python manage.py migrate
* python manage.py rqworker (запуск асинхронного worker)
* python manage.py createsuperuser 

После, необходимо заполнить БД принтерами (fixtures) для магазинов:
* python manage.py loaddata printer_data.json


Теперь вы можете начать взаимодействовать с сервисом.
* python manage.py runserver
### API points:

1) Создание чеков для заказа -
**/api/create_checks/**
#### Поля для заполнения (POST-запрос)
в body -> raw -> json-формат
* order
```
В качестве примера:
{
    "order": {
        "id": 24,
        "price": 1500,
        "items": [
            {
            "name": "Пицца",
            "quantity": 2,
            "unit_price": 100
            },
            {
            "name": "Хлеб",
            "quantity": 1,
            "unit_price": 50
            },
            {
            "name": "Молоко",
            "quantity": 1,
            "unit_price": 80
            },
            {
            "name": "Кондиционер",
            "quantity": 2,
            "unit_price": 150
            },
            {
            "name": "Шампунь",
            "quantity": 3,
            "unit_price": 290
            }
        ],
        "address": "г. Бердянск, ул. Кропоткина, д. 15/1, кв. 159",
        "client": {
            "name": "Андрей",
            "phone": 89159153344
        },
        "point_id": 1
    }
}
```
2) Список доступных чеков на печать - **/api/new_checks/**
#### Для просмотра списка чеков необходимо заполнить (GET-запрос)
в Params
* api_key

#### api_key можно найти через админ-панель в моделях Printer, 
пример: "q4x4JfCEwcm9EQkwT8O4gmKHAPfQJqxV"
3) PDF-чек на печать- **/api/check/**
#### Поля для заполнения (GET-запрос)
в Params
* api_key
* сheck_id


#### в качестве тестирования прошу использовать приложение postman, либо сайт https://www.postman.com/
