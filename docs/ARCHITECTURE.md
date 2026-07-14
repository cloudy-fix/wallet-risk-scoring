# Wallet Risk Scoring Architecture

## Purpose

Risk scoring engine for Ethereum wallets using Compound/Covalent transaction signals.

## Stack

Python, Requests, Pandas, NumPy, tqdm

## System Context

```mermaid
flowchart LR
    User["Wallet list and Covalent transaction data"] --> App["Feature extraction and risk scoring script"]
    App --> Data["Wallet transactions, Compound labels, gas/activity metrics"]
    App --> Output["wallet_scores.csv and risk analysis"]
    Data --> Output
```
## Runtime Workflow

```mermaid
flowchart TD
    S1["Load wallet list"] --> S2["Fetch wallet transactions"]
    S2["Fetch wallet transactions"] --> S3["Extract risk features"]
    S3["Extract risk features"] --> S4["Normalize and score wallets"]
    S4["Normalize and score wallets"] --> S5["Export score CSV"]
```
## Production Readiness Notes

- Keep secrets in environment variables and commit only .env.example templates.
- Keep generated files, dependency folders, caches, and local databases out of version control.
- Run the GitHub Actions workflow before presenting or deploying changes.
- Update this document when the source layout, dependencies, or deployment model changes.

## Review Checklist

- Architecture diagram matches current source files.
- Workflow diagram matches the main user or data path.
- README links to this architecture document.
- CI workflow validates the project on every push and pull request.

