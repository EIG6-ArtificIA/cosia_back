from django.contrib.auth.models import User, Group
from predictions_map.models import Department, DepartmentData
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
            "id",
            "number",
            "name",
            "status",
            "geom",
        ]


class DepartmentDataSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.StringRelatedField(source="__str__")

    class Meta:
        model = DepartmentData
        fields = [
            "name",
            "year",
            "download_link",
        ]
        depth = 1


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
