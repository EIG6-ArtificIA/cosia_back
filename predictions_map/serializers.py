from django.contrib.auth.models import User, Group
from predictions_map.models import Department
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = [
            "number",
            "name",
            "status",
            "geom",
        ]


class DepartmentDataSerializer(serializers.HyperlinkedModelSerializer):
    pass
    # class Meta:
    #     model = Department
    #     fields = [
    #         "number",
    #         "name",
    #         "status",
    #         "geom",
    #     ]


class DepartmentDataDownloadSerializer(serializers.HyperlinkedModelSerializer):
    pass
    # TODO
    # class Meta:
    #     model = Department
    #     fields = [
    #         "number",
    #         "name",
    #         "status",
    #         "geom",
    #     ]
