from django.urls import path
from .views import CurrentWeatherView, ForecastView

urlpatterns = [
    path('weather/current', CurrentWeatherView.as_view()),
    path('weather/forecast', ForecastView.as_view()),
]
