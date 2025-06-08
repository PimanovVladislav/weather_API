# Weather API

## Описание

Данный проект реализует REST API для получения текущей погоды и прогноза на ближайшие дни.

### Используемые внешние сервисы

- [OpenWeatherMap](https://openweathermap.org/api) — используется для получения реальных данных о погоде (текущая погода и прогноз).

Для работы необходимо получить API-ключ на сайте OpenWeatherMap и указать его в файле `.env` (создать на основе `.env.template`).

---

## Эндпоинты

- `GET /api/weather/current?city=CityName` — текущая температура и локальное время.
- `GET /api/weather/forecast?city=CityName&date=dd.MM.yyyy` — прогноз температуры на указанную дату.
- `POST /api/weather/forecast` — переопределение прогноза (сохраняется в базе).
    Формат тела запроса
- {
  "city": "Berlin",
  "date": "11.06.2025",
  "min_temperature": 10.0,
  "max_temperature": 18.5
}

---

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
