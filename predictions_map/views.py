from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from predictions_map.serializers import (
    UserSerializer,
    GroupSerializer,
    DepartmentSerializer,
    DepartmentDataSerializer,
    DepartmentDataDownloadSerializer,
)
from predictions_map.models import Department, DepartmentData


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


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


@api_view(["GET"])
def department_data_list(request):
    if request.method == "GET":
        department_data = DepartmentData.objects.all()
        serializer_context = {
            "request": request,
        }
        serializer = DepartmentDataSerializer(
            department_data, many=True, context=serializer_context
        )
        return Response(serializer.data)


@api_view(["GET"])
def department_data_detail(request, pk):
    try:
        department_data = DepartmentData.objects.get(pk=pk)
    except DepartmentData.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = DepartmentDataSerializer(department_data)
        return JsonResponse(serializer.data)


@api_view(["POST"])
def department_data_download_list(request):
    """
    Create a department data download.
    """
    if request.method == "POST":
        serializer = DepartmentDataDownloadSerializer(data=request.data)
        print(serializer)
        print("---")

        if serializer.is_valid():
            print(serializer)
            serializer.save()
            # TODO add an information : data download link
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
