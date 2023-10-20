from predictions_map.models import Department


def getAllDepartments():
    return Department.objects.all()
