from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Department

predictionsmap_mapping = {"name": "NOM", "geom": "MULTIPOLYGON", "number": "INSEE_DEP"}

french_departments = (
    Path(__file__).resolve().parent / "data" / "french_metropolitan_departments.gpkg"
)


def run(verbose=True):
    lm = LayerMapping(
        Department, french_departments, predictionsmap_mapping, transform=False
    )
    lm.save(strict=True, verbose=verbose)
