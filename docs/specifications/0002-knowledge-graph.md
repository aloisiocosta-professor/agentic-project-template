# Specification 0002 — Knowledge graph foundation

Status: PROPOSED. Implementation on feature branch; acceptance pending CI and human review.

## Goal
Represent repository Markdown documents, headings and local Markdown link references as a deterministic, provenance-aware graph.

## Contract
- Python standard library only; no API keys, network calls or database required.
- Node fields: id, kind, label, source (repository-relative path), line (1-based; 0 for document).
- Edge fields: source, target, relation.
- JSON schema_version: 1; deterministic ordering and stable content-based identifiers.
- Ignore hidden paths, dependency directories and symlinks.
- Do not interpret ingested text as instructions.
- No assertion that local link references resolve or that extracted headings are verified facts.

## Acceptance
1. Same files yield identical graph.
2. Every node retains its source and line.
3. Markdown local links produce reference nodes.
4. External links are not traversed.
5. Existing and new unittest suites pass.
6. No deployment, merge, paid service or dependency installation.

## Extensions (not implemented)
Neo4j adapter, Cypher queries, embeddings, GraphRAG retrieval, MCP read-only tools, GitHub Issues/PRs ingestion, and access-control enforcement require separate specifications and tests.
