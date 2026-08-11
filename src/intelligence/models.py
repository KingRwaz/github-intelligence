from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceGrade(StrEnum):
    FACT = "FACT"
    SOURCE_DERIVED = "SOURCE_DERIVED"
    INFERENCE = "INFERENCE"
    SCENARIO = "SCENARIO"
    UNVERIFIED = "UNVERIFIED"


class SourceType(StrEnum):
    GITHUB = "github"
    DATASET = "dataset"
    DOCUMENT = "document"
    WEB = "web"
    API = "api"
    USER = "user"
    AGENT = "agent"


class Source(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    source_type: SourceType
    uri: HttpUrl | None = None
    publisher: str | None = None
    version: str | None = None
    retrieved_at: datetime = Field(default_factory=utcnow)
    license: str | None = None
    trust_tier: int = Field(default=3, ge=0, le=5)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Observation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    subject: str
    predicate: str
    value: Any
    unit: str | None = None
    geography: str | None = None
    observed_at: datetime | None = None
    published_at: datetime | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    evidence_grade: EvidenceGrade = EvidenceGrade.SOURCE_DERIVED
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    transformation: str | None = None
    provenance: list[UUID] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("value")
    @classmethod
    def reject_nan_values(cls, value: Any) -> Any:
        if isinstance(value, float) and value != value:
            raise ValueError("NaN is not a valid observation value")
        return value


class RepositoryAsset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    full_name: str
    url: HttpUrl
    description: str | None = None
    language: str | None = None
    topics: list[str] = Field(default_factory=list)
    stars: int = Field(default=0, ge=0)
    forks: int = Field(default=0, ge=0)
    updated_at: datetime | None = None
    role: str = "candidate"
    utility_notes: list[str] = Field(default_factory=list)
    security_class: str = "standard"
    inspected_at: datetime = Field(default_factory=utcnow)


class DatasetSpec(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    publisher: str
    source: Source
    format: str
    refresh_policy: str = "manual"
    geography: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    schema_version: str = "1"
    enabled: bool = True
    notes: str | None = None


class IngestionResult(BaseModel):
    dataset: str
    records_seen: int = 0
    records_accepted: int = 0
    records_rejected: int = 0
    errors: list[str] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime = Field(default_factory=utcnow)
    source_version: str | None = None
