from predictions_map.models import Territory

def getAllTerritories():
    return Territory.objects.all()
