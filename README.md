# Synology NAS Migration Playbook

A safety-first reference for reorganizing a Synology NAS while preserving media services, download-client state, container configuration, and a credible rollback path.

This repository is a generalized playbook, not an export of a particular NAS. It contains no operational report tree, torrent inventory, credentials, application databases, recovery archives, or private infrastructure map.

## What this covers

- Storage discovery and migration sequencing
- qBittorrent relocation without losing resumability
- Cross-seed-aware handling of shared payloads and hardlinks
- Sonarr and Radarr path remediation
- Docker Compose relocation and validation
- Selective retirement of a legacy staging root
- Synology filesystem and ACL remediation
- Event-driven IPv6 automation recovery
- Disaster-recovery design, evidence capture, and closeout gates

## The core rule

Treat every destructive step as the last stage of an evidence pipeline:

```text
discover -> classify -> copy -> verify -> rebind -> validate -> quarantine -> soak -> retire -> prove
```

Copying bytes is not enough. A migration is complete only when applications resolve the new paths, protected exceptions still work, rollback material is usable, and the final state can be independently checked. Passing migration validation establishes readiness, not automatic deletion authorization:

- **Quarantine**: Reversible isolation of legacy paths from active service configuration.
- **Soak**: Observation period covering scheduled background activity while old data remains recoverable.
- **Retire**: Permanent removal only after reference absence and explicit authorization gates pass.

## Relationship to Storage Director toolkit

This repository focuses on operational migration methodology, procedural playbooks, and safety gates. The companion repository `nas-storage-director-toolkit` provides an independent reference implementation for policy-driven storage allocation and state monitoring. This playbook does not require or depend on that toolkit.

## Start here

1. Read [Architecture](docs/architecture.md) and [Migration strategy](docs/migration-strategy.md).
2. Build a path map from [the example](examples/path-mapping.example.md).
3. Inventory qBittorrent, hardlinks, ARR roots, Compose mounts, permissions, scheduled tasks, and backups.
4. Rehearse one small cohort and record objective gates.
5. Run the relevant domain playbooks before retiring any source path.
6. Finish with [Validation and closeout](docs/validation-and-closeout.md).

## Repository map

- `docs/` — domain playbooks and lessons
- `examples/` — placeholder-only configuration examples
- `scripts/` — small, dependency-free validation helpers
- `prompts/` — reusable, sanitized AI-agent briefs

## Safety boundaries

Examples use placeholders such as `<NAS_HOST>`, `<MEDIA_ROOT>`, `<DOWNLOAD_ROOT>`, `<STAGING_ROOT>`, `<API_KEY>`, `<TRACKER>`, and `<TORRENT_HASH>`. Replace them only in a private working copy. Never commit live configuration or raw state files.

The scripts default to read-only checks. Review commands for your DSM version, filesystem, container runtime, and applications before use. Snapshots are not backups, hardlinks are not duplicates, and a green application UI is not proof of data integrity.

## License

MIT. See [LICENSE](LICENSE).
