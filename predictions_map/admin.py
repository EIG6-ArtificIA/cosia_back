from django.contrib import admin
from .models import Department, DepartmentData, DepartmentDataDownload


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["number", "name", "status"]


class DepartmentDataAdmin(admin.ModelAdmin):
    list_display = ["department", "year", "s3_object_name", "file_size", "zip_size"]

    def delete_queryset(self, request, queryset):
        for department_data in queryset:
            department_data.delete()


class DepartmentDataDownloadAdmin(admin.ModelAdmin):
    list_display = [
        "department_data",
        "username",
        "organization",
        "email",
        "created_at",
    ]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentData, DepartmentDataAdmin)
admin.site.register(DepartmentDataDownload, DepartmentDataDownloadAdmin)
