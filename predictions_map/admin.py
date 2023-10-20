from django.contrib import admin
from .models import Department, DepartmentData, DepartmentDataDownload


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["number", "name", "status"]


class DepartmentDataAdmin(admin.ModelAdmin):
    list_display = ["department", "year", "download_link"]


class DepartmentDataDownloadAdmin(admin.ModelAdmin):
    list_display = ["department_data", "username", "organisation", "email"]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentData, DepartmentDataAdmin)
admin.site.register(DepartmentDataDownload, DepartmentDataDownloadAdmin)
