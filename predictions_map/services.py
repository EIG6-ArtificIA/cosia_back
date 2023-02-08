from predictions_map.models import RASTER_VALUE_TO_LABEL, PredictedArea


def getAllObjectsFromType(type):
    raster_val = list(RASTER_VALUE_TO_LABEL.keys())[list(RASTER_VALUE_TO_LABEL.values()).index(type)]
    return PredictedArea.objects.filter(raster_val=raster_val)