from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Iterable

from .models import IngestionResult, Observation


class Ingestor(ABC):
    """Contract for every data connector. Connectors return observations, never opaque text."""

    name: str

    @abstractmethod
    def fetch(self) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, rows: Iterable[dict[str, Any]]) -> Iterable[Observation]:
        raise NotImplementedError

    def run(self) -> tuple[IngestionResult, list[Observation]]:
        started = datetime.now(timezone.utc)
        errors: list[str] = []
        accepted: list[Observation] = []
        seen = 0
        try:
            rows = list(self.fetch())
            seen = len(rows)
            accepted = list(self.normalize(rows))
        except Exception as exc:  # connector errors are reported, not hidden
            errors.append(f"{type(exc).__name__}: {exc}")
        result = IngestionResult(
            dataset=self.name,
            records_seen=seen,
            records_accepted=len(accepted),
            records_rejected=max(0, seen - len(accepted)),
            errors=errors,
            started_at=started,
        )
        return result, accepted
