from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import  PredictionsMap

predictionsmap_mapping = {
    'raster_val': 'raster_val',
    'geom': 'MULTIPOLYGON',
}

predictionsmap_shp = Path(__file__).resolve().parent / 'data' / 'data_Aubiet_25_05.shp'

def run(verbose=True):
    lm = LayerMapping(PredictionsMap, predictionsmap_shp, predictionsmap_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)