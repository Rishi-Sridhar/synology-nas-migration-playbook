# Staging Retirement

A legacy staging root often contains a mixture of obsolete copies, live torrent payloads, rollback data, and application-visible paths. Retire it by manifest, not by directory.

## Classification

Assign every leaf to one state:

- `DELETE` — proven redundant and unreferenced
- `KEEP` — an active dependency or explicit rollback asset
- `UNKNOWN` — incomplete evidence; automatically protected

The default is `UNKNOWN`. Require coverage accounting so the sum of classified files equals the fresh filesystem inventory.

## Execution gates

Before deletion:

1. Re-scan application references and container mounts.
2. Reconcile qBittorrent save paths and cross-seed groups.
3. Re-stat each target and compare identity, size, and modification time with the manifest.
4. Confirm no active writes beneath the root.
5. Verify protected sets and parent paths cannot match the delete scope.
6. Run a dry pass that produces counts and bytes but performs no mutation.

Execute exact file deletions, record one receipt per target, and stop on the first unexpected condition. Remove empty directories only after a second inventory. Never follow symlinks during retirement.

## Afterward

Mount a required legacy bind read-only. Confirm every retained consumer still works. Compare expected and observed file counts and bytes, then verify freed space separately; snapshots, hardlinks, and filesystem metadata can make those numbers differ.
