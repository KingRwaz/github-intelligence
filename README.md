# GitHub Intelligence

A provenance-first intelligence and agent orchestration platform built from the user's curated open-source stack.

## Mission

Unify repositories, documents, datasets, market intelligence, research and agent capabilities into a governed system that can ingest, normalize, validate, retrieve, reason and monitor without silently converting assumptions into facts.

## Core architecture

`Sources -> Ingestion -> Normalization -> Provenance -> Storage -> Retrieval -> Agents -> Intelligence Outputs`

### Initial capabilities

- GitHub repository intelligence
- Document ingestion boundary for MinerU/OCR pipelines
- Dataset registry and provenance model
- Structured event/observation storage
- Hybrid retrieval adapters for Qdrant/Neo4j
- Agent orchestration boundary for OpenClaw/LangChain/LlamaIndex/AutoGen/MiroShark
- Evidence grades: FACT, SOURCE_DERIVED, INFERENCE, SCENARIO, UNVERIFIED
- Security-sensitive capability isolation
- Health and ingestion observability

## Repository policy

This project does not blindly install all 364+ repositories. Repositories are treated as source components, reference implementations, adapters, or optional modules. Each component must pass provenance, compatibility, security and utility checks before promotion to the runtime.

## Data policy

Every external observation should retain source identity, retrieval time, publication/observation time, dataset version where available, geography/entity, units, transformation history and confidence/provenance metadata.

## Status

Phase 1 foundation: repository and dataset intelligence model, ingestion contracts, provenance model, API skeleton and tests.
