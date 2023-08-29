from .models import PredictedArea
from rest_framework import viewsets
from .serializers import PredictedAreaSerializer


class PredictedAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PredictedArea.objects.all()
    serializer_class = PredictedAreaSerializer

