from rest_framework import serializers

class TimeSeriesPointSerializer(serializers.Serializer):
    datetime_utc = serializers.DateTimeField()
    value = serializers.FloatField()
    unit = serializers.CharField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    sensor_id = serializers.CharField(required=False, allow_null=True)
    lat = serializers.FloatField(required=False, allow_null=True)
    lon = serializers.FloatField(required=False, allow_null=True)
