from django.contrib.gis.db import models

class PredictionsMap(models.Model):
    raster_val = models.BigIntegerField()
    geom = models.MultiPolygonField(srid=2154)
