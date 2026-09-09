# Cleanup Review Agent Prompt

Review `<STAGING_ROOT>` for selective retirement without changing the live system.

Build a fresh inventory and classify every leaf as `DELETE`, `KEEP`, or `UNKNOWN`. Default to `UNKNOWN`. Correlate path consumers across qBittorrent, cross-seed tooling, Sonarr, Radarr, media servers, container mounts, scripts, scheduled tasks, snapshots, and backups.

For each proposed deletion, require:

- Stable file identity and metadata
- No active writer
- No sole active torrent or media-library reference
- Hardlink-aware physical reclaim estimate
- Verified destination or explicit proof that no copy is required
- Rollback or recovery pointer

Output a review table and a machine-readable proposed manifest, but do not delete anything. Exclude torrent hashes, tracker names, media titles, credentials, private paths, and account identifiers from any shareable summary. Use generic record IDs.

Reject broad recursive deletion. Require full classification coverage, protected-prefix tests, a dry run, fresh pre-mutation restat, per-target receipts, stop-on-first-error behavior, and post-delete reconciliation.
