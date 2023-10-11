from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Department

predictionsmap_mapping = {
    "name": "nom",
    "geom": "POLYGON",
}

predictionsmap_shp = (
    Path(__file__).resolve().parent
    / "data"
    / "Saint-Nazaire"
    / "emprise_SaintNazaire_agglo.shp"
)


def run(verbose=True):
    lm = LayerMapping(
        Department, predictionsmap_shp, predictionsmap_mapping, transform=False
    )
    lm.save(strict=True, verbose=verbose)
