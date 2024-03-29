from django.urls import path
from predictions_map import views

urlpatterns = [
    path("departments/", views.department_list),
    path("departments/<int:pk>/", views.department_detail),
    path("department-data/", views.department_data_list),
    path(
        "department-data/<int:pk>/",
        views.department_data_detail,
        name="department_data_detail",
    ),
    path("department-data-downloads/", views.department_data_download_list),
]
