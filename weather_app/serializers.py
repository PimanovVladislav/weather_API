from rest_framework import serializers
from datetime import datetime, date, timedelta

DATE_FORMAT = "%d.%m.%Y"

class CurrentWeatherSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)

class ForecastGetSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.CharField(required=True)

    def validate_date(self, value):
        try:
            dt = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise serializers.ValidationError("Date must be in format dd.MM.yyyy")
        today = date.today()
        if dt < today:
            raise serializers.ValidationError("Date cannot be in the past")
        if dt > today + timedelta(days=10):
            raise serializers.ValidationError("Date cannot be more than 10 days in the future")
        return dt

class ForecastPostSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    min_temperature = serializers.FloatField(required=True)
    max_temperature = serializers.FloatField(required=True)

    def validate_date(self, value):
        try:
            dt = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise serializers.ValidationError("Date must be in format dd.MM.yyyy")
        today = date.today()
        if dt < today:
            raise serializers.ValidationError("Date cannot be in the past")
        if dt > today + timedelta(days=10):
            raise serializers.ValidationError("Date cannot be more than 10 days in the future")
        return dt

    def validate(self, data):
        if data['min_temperature'] > data['max_temperature']:
            raise serializers.ValidationError("min_temperature cannot be greater than max_temperature")
        return data
