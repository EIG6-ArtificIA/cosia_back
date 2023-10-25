from django.contrib.auth.models import User, Group
from predictions_map.models import Department, DepartmentData, DepartmentDataDownload
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


class DepartmentDataSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="__str__")

    class Meta:
        model = DepartmentData
        fields = [
            "name",
            "year",
            "download_link",
            "department",
        ]

    def to_representation(self, instance):
        self.fields["department"] = DepartmentSerializer(read_only=True)
        return super(DepartmentDataSerializer, self).to_representation(instance)


class DepartmentDataDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentDataDownload
        fields = [
            "department_data",
            "username",
            "organisation",
            "email",
        ]

    def to_representation(self, instance):
        self.fields["department_data"] = DepartmentDataSerializer(read_only=True)
        return super(DepartmentDataDownloadSerializer, self).to_representation(instance)
