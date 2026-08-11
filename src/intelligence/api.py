from __future__ import annotations

from fastapi import FastAPI, Query

from .registry import seed_registry
from .store import IntelligenceStore

app = FastAPI(title="GitHub Intelligence", version="0.1.0")
store = IntelligenceStore()
seed_registry(store)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "github-intelligence"}


@app.get("/v1/observations")
def observations(limit: int = Query(default=100, ge=1, le=1000)) -> dict:
    return {"items": store.recent_observations(limit), "count": limit}


@app.get("/v1/capabilities")
def capabilities() -> dict:
    return {
        "ingestion": ["github", "documents", "datasets"],
        "storage": ["duckdb"],
        "optional_retrieval": ["qdrant", "neo4j"],
        "orchestration": ["openclaw", "langchain", "llamaindex", "autogen", "miroshark"],
        "evidence_grades": ["FACT", "SOURCE_DERIVED", "INFERENCE", "SCENARIO", "UNVERIFIED"],
    }
