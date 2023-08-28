from django.contrib.gis.db import models


class PredictedArea(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    geom = models.MultiPolygonField(srid=2154)
    status = models.CharField(max_length=100, null=False, blank=False)