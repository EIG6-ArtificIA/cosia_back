from django.contrib.gis.db import models

RASTER_VALUE_TO_LABEL = {
    0:"Batiment",
    1:"Zone permeable",
    2:"Zone impermeable",
    3:"Piscine",
    4:"Sol nu",
    5:"Surface Eau",
    6:"Neige",
    7:"Conifere",
    8:"Coupe",
    9:"Feuillu",
    10:"Broussaille",
    11:"Vigne",
    12:"Culture",
    13:"Terre labouree",
    15:"Autre",
    17:"Pelouse",
    18:"Serre",
    19:"Autre",
}

class PredictedArea(models.Model):
    raster_val = models.BigIntegerField()
    geom = models.MultiPolygonField(srid=2154)

    @property
    def type(self):
        return RASTER_VALUE_TO_LABEL[self.raster_val]