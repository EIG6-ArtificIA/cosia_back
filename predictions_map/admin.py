from django.contrib import admin
from .models import Territory

admin.site.register(Territory, admin.ModelAdmin)