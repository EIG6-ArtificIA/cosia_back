from django.contrib import admin
from .models import Department, DepartmentData, DepartmentDataDownload


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["number", "name", "status"]


class DepartmentDataAdmin(admin.ModelAdmin):
    list_display = ["department", "year", "download_link", "fileSize", "zipSize"]


class DepartmentDataDownloadAdmin(admin.ModelAdmin):
    list_display = ["department_data", "username", "organization", "email"]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentData, DepartmentDataAdmin)
admin.site.register(DepartmentDataDownload, DepartmentDataDownloadAdmin)
