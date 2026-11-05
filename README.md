# Agentic Project Template

Reusable starter for specification-driven development with ChatGPT, Codex, and GitHub Actions. No external AI API is required by the default CI.

## Start
1. Use this directory as the root of a new repository (or GitHub template repository).
2. Replace placeholders in `docs/specifications/0001-project.md`.
3. Define acceptance tests in `tests/`.
4. Review `AGENTS.md` and `harness/autonomy.json` for project-specific policies.
5. Run `python -m unittest discover -s tests -v` and `python scripts/validate_template.py`.
6. Configure branch protection, required status checks, and approval rules in GitHub Settings; files alone do not enforce them.

## Operating model
ChatGPT: research and specification. Codex: authorized code changes. GitHub Issues/PRs: traceability. GitHub Actions: independent checks. Human: approvals and releases.

## Scope
The baseline validates documentation and a small policy contract; it does not implement a secure sandbox, enforce permissions on Codex, or deploy software. Extend the CI for the project's language and threat model.
