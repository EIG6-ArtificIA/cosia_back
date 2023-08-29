from .models import PredictedArea
from rest_framework import serializers


class PredictedAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PredictedArea
        fields = ['name', 'geom', 'status']
