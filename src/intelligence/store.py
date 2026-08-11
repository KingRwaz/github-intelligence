from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import duckdb

from .models import DatasetSpec, Observation, RepositoryAsset, Source


class IntelligenceStore:
    """Small deterministic storage core; DuckDB is the local system of record."""

    def __init__(self, path: str = "data/intelligence.duckdb") -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self):
        return duckdb.connect(self.path)

    def _init(self) -> None:
        with self._conn() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id UUID PRIMARY KEY, name VARCHAR, source_type VARCHAR,
                    uri VARCHAR, publisher VARCHAR, version VARCHAR,
                    retrieved_at TIMESTAMPTZ, license VARCHAR, trust_tier INTEGER,
                    metadata JSON
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id UUID PRIMARY KEY, source_id UUID, subject VARCHAR,
                    predicate VARCHAR, value JSON, unit VARCHAR, geography VARCHAR,
                    observed_at TIMESTAMPTZ, published_at TIMESTAMPTZ,
                    valid_from TIMESTAMPTZ, valid_to TIMESTAMPTZ,
                    evidence_grade VARCHAR, confidence DOUBLE,
                    transformation VARCHAR, provenance JSON, metadata JSON
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    id UUID PRIMARY KEY, full_name VARCHAR UNIQUE, url VARCHAR,
                    description VARCHAR, language VARCHAR, topics JSON,
                    stars BIGINT, forks BIGINT, updated_at TIMESTAMPTZ,
                    role VARCHAR, utility_notes JSON, security_class VARCHAR,
                    inspected_at TIMESTAMPTZ
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS datasets (
                    id UUID PRIMARY KEY, name VARCHAR, publisher VARCHAR,
                    source_id UUID, format VARCHAR, refresh_policy VARCHAR,
                    geography JSON, domains JSON, schema_version VARCHAR,
                    enabled BOOLEAN, notes VARCHAR
                )
            """)

    def add_source(self, source: Source) -> None:
        with self._conn() as db:
            db.execute("INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [str(source.id), source.name, source.source_type.value,
                        str(source.uri) if source.uri else None, source.publisher,
                        source.version, source.retrieved_at, source.license,
                        source.trust_tier, json.dumps(source.metadata)])

    def add_observations(self, observations: Iterable[Observation]) -> int:
        count = 0
        with self._conn() as db:
            for o in observations:
                db.execute("INSERT OR REPLACE INTO observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [str(o.id), str(o.source_id), o.subject, o.predicate,
                            json.dumps(o.value), o.unit, o.geography, o.observed_at,
                            o.published_at, o.valid_from, o.valid_to,
                            o.evidence_grade.value, o.confidence, o.transformation,
                            json.dumps([str(x) for x in o.provenance]), json.dumps(o.metadata)])
                count += 1
        return count

    def upsert_repository(self, repo: RepositoryAsset) -> None:
        with self._conn() as db:
            db.execute("INSERT OR REPLACE INTO repositories VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [str(repo.id), repo.full_name, str(repo.url), repo.description,
                        repo.language, json.dumps(repo.topics), repo.stars, repo.forks,
                        repo.updated_at, repo.role, json.dumps(repo.utility_notes),
                        repo.security_class, repo.inspected_at])

    def register_dataset(self, dataset: DatasetSpec) -> None:
        self.add_source(dataset.source)
        with self._conn() as db:
            db.execute("INSERT OR REPLACE INTO datasets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [str(dataset.id), dataset.name, dataset.publisher,
                        str(dataset.source.id), dataset.format, dataset.refresh_policy,
                        json.dumps(dataset.geography), json.dumps(dataset.domains),
                        dataset.schema_version, dataset.enabled, dataset.notes])

    def recent_observations(self, limit: int = 100) -> list[dict]:
        with self._conn() as db:
            rows = db.execute("SELECT * FROM observations ORDER BY COALESCE(observed_at, published_at) DESC NULLS LAST LIMIT ?", [limit]).fetchall()
            cols = [d[0] for d in db.description]
            return [dict(zip(cols, row)) for row in rows]
