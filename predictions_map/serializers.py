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


class DepartmentDataSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.StringRelatedField(source="__str__")

    class Meta:
        model = DepartmentData
        fields = [
            "name",
            "year",
            "download_link",
        ]


class DepartmentDataDownloadSerializer(serializers.HyperlinkedModelSerializer):
    department_data = serializers.HyperlinkedRelatedField(
        view_name="department_data_detail"
    )

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
