# Cleanup Review Agent Prompt

Review `<STAGING_ROOT>` for selective retirement without changing the live system.

Rules:

1. Build a fresh inventory and classify every leaf as `DELETE`, `KEEP`, or `UNKNOWN`. Default to `UNKNOWN`.
2. Stop on any `UNKNOWN` classification; incomplete evidence protects the file from retirement.
3. In this workflow, `DELETE` designates *eligible for retirement workflow*, never immediate destruction. Never jump directly from stale classification to permanent deletion.
4. Respect declared protected namespaces: never scan or recurse into recovery bundles, backup roots, filesystem snapshots, or quarantine zones.
5. Correlate path consumers across qBittorrent, cross-seed tooling, Sonarr, Radarr, media servers, container mounts, scripts, scheduled tasks, snapshots, and backups.
6. Use bounded scans rather than open-ended recursive traversal.
7. For each candidate cohort, propose:
   - A reversible quarantine destination (e.g., `<QUARANTINE_ROOT>/<cohort-timestamp>/`).
   - Explicit soak criteria (covering at least one full operational cycle of scheduled tasks, automated grabs, and backups).
   - Reference absence proofs across Compose files, runtime `docker inspect` mounts, scheduled tasks, and application databases.
   - Hardlink-aware physical storage reclaim estimates.
   - Verified active replacement data locations.
   - Intact rollback and recovery pointers.
8. Output a review table and a machine-readable quarantine manifest, but do not modify or delete anything. Exclude torrent hashes, tracker names, media titles, credentials, private paths, and account identifiers from any shareable summary. Use generic record IDs.
9. Reject broad recursive unlinking. Emphasize that passing all validation gates establishes deletion eligibility, not deletion authorization. Permanent purge requires an explicit, separate destructive authorization from the operator.
