# Security and capability policy

The system uses least privilege and explicit capability classes.

## Capability classes

- `standard`: normal ingestion, analysis and retrieval.
- `sensitive`: connectors that may expose personal, financial or operationally sensitive data.
- `security-research`: defensive security research, isolated from normal autonomous execution.
- `restricted`: capabilities that can cause external side effects or interact with protected systems.

Restricted and security-research capabilities are never enabled merely because a repository is present in the user's stack. They require explicit configuration, scoped credentials and an auditable execution boundary.

## Evidence policy

Agents must not present `INFERENCE`, `SCENARIO`, or `UNVERIFIED` material as established fact. External observations must retain provenance and timestamps.
