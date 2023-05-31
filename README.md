# Тестовое задание WelbeX


## Описание проекта
В этом проекте я реализовал API для работы логистики по перевозке грузов. В проекте используются Django + DRF, PostgreSQL
в качестве БД. Проект запускается в контейнерах Docker

## Настройка окружения
При запуске локально настройте окружение и установите зависимости:
```shell script
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

## Запуск проекта
Запуск осуществляется командой:
```shell script
docker-compose up -d
```

## Создание superuser для работы с моделями в Django Admin Panel
```shell script
docker-compose run app python manage.py createsuperuser
```

## Описание API
#### 1) Администрационная панель: [*Admin panel*](http://0.0.0.0:8000/admin);
#### 2) Создание груза (локации груза передаём zip-кодами в теле запроса): [*GET logistics/cargos/create*](http://0.0.0.0:8000/logistics/cargos/create);
- *input data*: 
```json
{
  "pick_up_zip": "00002",
  "delivery_zip": "99998",
  "weight": "500",
  "description": "cargo description"
}
```
- *result*:
```json
{
  "status": "success",
  "created": "Cargo #1"
}
```
- *error*:
```json
{
  "error": "error_description"
}
```
#### 2) Список грузов с количеством ближайших машин (< 450 миль): [*GET logistics/cargos*](http://0.0.0.0:8000/logistics/cargos/);
- *result*:
```json
[
  {
    "id": 1,
    "pick_up_location": 33788,
    "delivery_location": 33788,
    "nearest_trucks": [
      1
    ]
  }
]
```
- *error*:
```json
{
  "error": "error_description"
}
```
#### 3) Получение информации о конкретном грузе по ID + информация об автомобилях и дистанциях до них: [*GET logistics/cargos/[pk]*](http://0.0.0.0:8000/logistics/cargos/-pk-);
- *result*:
```json
{
  "id": 4,
  "pick_up_location": 33788,
  "delivery_location": 33788,
  "weight": 32,
  "description": "dsds",
  "trucks": [
    {
      "truck": "1019P",
      "distance": 0
    },
    {
      "truck": "8075R",
      "distance": 2756
    }
  ]
}
```
- *error*:
```json
{
  "error": "error_description"
}
```
#### 4) Редактирование груза по ID (вес и описание передаём в теле запроса): [*GET logistics/cargos/[pk]/update*](http://0.0.0.0:8000/logistics/cargos/-pk-/update);
- *input data*: 
```json
{
  "weight": 500,
  "description": "cargo description"
}
```
- *result*:
```json
{
  "id": 5,
  "weight": 500,
  "description": "cargo description"
}
```
- *error*:
```json
{
  "error": "error_description"
}
```
#### 5) Удаление груза по ID: [*GET logistics/cargos/[pk]/destroy*](http://0.0.0.0:8000/logistics/cargos/-pk-/destroy);
- *result*:
```json
{
  "success": "Cargo #0 was deleted"
}
```
- *error*:
```json
{
  "error": "error_description"
}
```
#### 6) Редактирование машины по ID (локация автомобиля изменяется через zip-код): [*GET logistics/trucks/[pk]/update*](http://0.0.0.0:8000/logistics/trucks/-pk-/update);
- *input data*: 
```json
{
  "location_zip": "99929"
}
```
- *result*:
```json
{
  "success": "Truck #1019P saved with location \"Wrangell, AK 99929\""
}
```
- *error*:
```json
{
  "error": "error_description"
}
```
###### _Python 3.9.5_