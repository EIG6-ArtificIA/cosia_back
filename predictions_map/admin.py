from django.contrib import admin
from .models import PredictedArea

admin.site.register(PredictedArea, admin.ModelAdmin)