from predictions_map.models import Department, DepartmentData, DepartmentDataDownload
from rest_framework import serializers

from predictions_map.s3_client import S3Client


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
            "geom_geojson",
            "centroid_geojson",
        ]


class DepartmentDataSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DepartmentData
        fields = [
            "id",
            "year",
            "department",
            "file_size",
            "zip_size",
            "s3_download_url",
        ]

    s3_download_url = serializers.SerializerMethodField("get_s3_download_url")

    def get_s3_download_url(self, obj):
        if obj.s3_object_name is None:
            return ValueError("This Download Data has no s3_object_name")
        s3client = S3Client()

        return s3client.get_object_download_url(obj.s3_object_name)

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
