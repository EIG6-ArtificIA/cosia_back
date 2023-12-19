from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from predictions_map.serializers import (
    DepartmentSerializer,
    DepartmentDataSerializer,
    DepartmentDataDownloadSerializer,
)
from predictions_map.models import Department, DepartmentData


@api_view(["GET"])
def department_list(request):
    if request.method == "GET":
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def department_detail(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = DepartmentSerializer(department)
        return JsonResponse(serializer.data)


READ_ONLY_DEPARTMENT_DATA_FIELDS = [
    "id",
    "year",
    "department",
    "file_size",
    "zip_size",
]


# TODO Once front is using s3_object_name, remove if/else
@api_view(["GET"])
def department_data_list(request):
    if request.method == "GET":
        only_with_s3_object_name = request.query_params.get("only_with_s3_object_name")
        print(only_with_s3_object_name)
        if only_with_s3_object_name is None:
            department_data = DepartmentData.objects.all()
        else:
            department_data = DepartmentData.objects.exclude(
                Q(s3_object_name__exact="")
            )

        serializer_context = {"request": request}

        serializer = DepartmentDataSerializer(
            department_data,
            many=True,
            context=serializer_context,
            fields=READ_ONLY_DEPARTMENT_DATA_FIELDS,
        )
        return Response(serializer.data)


@api_view(["GET"])
def department_data_detail(request, pk):
    try:
        department_data = DepartmentData.objects.get(pk=pk)
    except DepartmentData.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = DepartmentDataSerializer(
            department_data, fields=READ_ONLY_DEPARTMENT_DATA_FIELDS
        )
        return JsonResponse(serializer.data)


@ratelimit(key="ip", rate="10/m")
@csrf_protect
@api_view(["POST"])
def department_data_download_list(request):
    if request.method == "POST":
        serializer = DepartmentDataDownloadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
