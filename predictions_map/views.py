from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from predictions_map.serializers import (
    UserSerializer,
    GroupSerializer,
    DepartmentSerializer,
)
from predictions_map.models import Department


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Departments to be viewed or edited
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
