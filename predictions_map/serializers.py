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


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DepartmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Department
        fields = [
            "number",
            "name",
            "status",
            "geom",
        ]


class DepartmentDataSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DepartmentData
        fields = [
            "id",
            "year",
            "download_link",
            "department",
        ]

    def to_representation(self, instance):
        self.fields["department"] = DepartmentSerializer(
            read_only=True, fields=("name", "number")
        )
        return super(DepartmentDataSerializer, self).to_representation(instance)


class DepartmentDataDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentDataDownload
        fields = [
            "department_data",
            "username",
            "organization",
            "email",
        ]

    def to_representation(self, instance):
        self.fields["department_data"] = DepartmentDataSerializer(read_only=True)
        return super(DepartmentDataDownloadSerializer, self).to_representation(instance)
