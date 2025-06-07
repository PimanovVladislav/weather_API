from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrentWeatherSerializer, ForecastGetSerializer, ForecastPostSerializer
from .models import OverriddenForecast
from .utils import get_current_weather, get_forecast
from datetime import datetime

DATE_FORMAT = "%d.%m.%Y"

class CurrentWeatherView(APIView):
    def get(self, request):
        serializer = CurrentWeatherSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']
        data, error = get_current_weather(city)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)

class ForecastView(APIView):
    def get(self, request):
        serializer = ForecastGetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']
        date_obj = serializer.validated_data['date']

        try:
            overridden = OverriddenForecast.objects.get(city__iexact=city, date=date_obj)
            return Response({
                "min_temperature": overridden.min_temperature,
                "max_temperature": overridden.max_temperature,
            })
        except OverriddenForecast.DoesNotExist:
            pass

        data, error = get_forecast(city, date_obj)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)

    def post(self, request):
        serializer = ForecastPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']
        date_obj = serializer.validated_data['date']
        min_temp = serializer.validated_data['min_temperature']
        max_temp = serializer.validated_data['max_temperature']

        obj, created = OverriddenForecast.objects.update_or_create(
            city__iexact=city,
            date=date_obj,
            defaults={
                "city": city,
                "date": date_obj,
                "min_temperature": min_temp,
                "max_temperature": max_temp
            }
        )
        return Response({"detail": "Forecast saved successfully."})
