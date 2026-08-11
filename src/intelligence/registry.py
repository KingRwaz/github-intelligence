from __future__ import annotations

from .models import DatasetSpec, Source, SourceType
from .store import IntelligenceStore


CORE_DATASETS = [
    DatasetSpec(
        name="World Bank Real-Time Food Prices - Uganda",
        publisher="World Bank",
        source=Source(name="World Bank RTFP", source_type=SourceType.DATASET,
                      uri="https://microdata.worldbank.org/catalog/8241", publisher="World Bank", trust_tier=5),
        format="API/CSV",
        refresh_policy="daily",
        geography=["Uganda"],
        domains=["agriculture", "food_prices", "markets"],
    ),
    DatasetSpec(
        name="FAOSTAT Agriculture and Food Data",
        publisher="FAO",
        source=Source(name="FAOSTAT", source_type=SourceType.DATASET,
                      uri="https://www.fao.org/faostat/", publisher="FAO", trust_tier=5),
        format="API/CSV",
        refresh_policy="on_release",
        geography=["global", "Uganda"],
        domains=["agriculture", "food", "trade", "production", "prices"],
    ),
    DatasetSpec(
        name="Uganda NAMIS",
        publisher="Government of Uganda",
        source=Source(name="NAMIS", source_type=SourceType.DATASET,
                      uri="https://namis.agriculture.go.ug/", publisher="MAAIF", trust_tier=5),
        format="web/API",
        refresh_policy="daily",
        geography=["Uganda"],
        domains=["agriculture", "markets", "weather", "value_chains"],
    ),
]


def seed_registry(store: IntelligenceStore) -> int:
    for dataset in CORE_DATASETS:
        store.register_dataset(dataset)
    return len(CORE_DATASETS)
