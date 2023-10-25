from django.urls import path
from predictions_map import views

urlpatterns = [
    path("departments/", views.department_list),
    path("departments/<int:pk>/", views.department_detail),
    path("department_data/", views.department_data_list),
    path("department_data_downloads/", views.department_data_download_list),
]
