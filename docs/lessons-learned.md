# Lessons Learned

## Evidence beats intuition

Storage names, media titles, and application labels are hints, not identities. Filesystem identity, content verification, application state, and fresh observations prevent confident but unsafe decisions.

## Separate registration from payload deletion

Removing a torrent registration and deleting its files are different operations. Keeping them separate is especially important for cross-seeds, hardlinks, and library-resident media.

## Canonical paths reduce future debt

Stable container paths and explicit download categories make host-volume changes less disruptive. After remediation, query every state surface for old prefixes; do not stop after editing the visible root folder.

## Preserve small ambiguities

Deleting tiny unknown Docker volumes or zero-reclaim hardlink names offers little benefit and disproportionate regression risk. An intentional exception is often the correct engineering result.

## Quarantine before irreversible purge

Never delete retired storage roots directly upon cutover. Move legacy roots into an isolated quarantine zone first. Quarantine makes the cutover reversible if latent consumers or unmigrated dependencies surface.

## Soak before retirement

A green dashboard immediately after migration does not guarantee that scheduled jobs will succeed. Enforce an explicit soak period covering at least one complete cycle of automated background tasks, library updates, and backups before moving from quarantine to deletion review.

## Prove mount and reference absence before purge

Before permanently unlinking quarantined data, perform bounded verification across Compose specifications, runtime `docker inspect` mounts, scheduled tasks, and application databases to prove zero remaining references to the legacy path.

## Path existence is not active mount exposure

Verifying that a directory exists on the host does not confirm that an application container mounts it, reaches the correct internal path, or holds sufficient effective UID/GID permissions. Verify the end-to-end exposure chain, not just host inodes.

## Treat live SQLite/WAL databases as application-owned state

Media applications running SQLite in WAL mode must not be inspected or modified with external database tools while active. Host-side queries against live WAL files can produce locking conflicts and dirty reads. Use application REST APIs, or stop the container cleanly and checkpoint the WAL before touching database files.

## Keep mutation scope narrow

Limit each migration operation to the specific cohort under change. Avoid restarting the host Docker daemon or cycling unrelated service stacks during incremental migrations. Narrow blast radiuses prevent cascading operational failures.

## Preserve rollback assets until formal closeout

Rollback manifests, database backups, and recovery bundles must remain intact and accessible throughout the entire migration process. Do not prune rollback material when an individual cohort succeeds; retain it until formal closeout sign-off.

## Separate evidence blemishes from correctness failures

Distinguish non-blocking observation blemishes (such as benign timestamp differences or regenerated cache files) from genuine correctness failures (such as missing bytes, hash mismatches, or permission errors). Document blemishes in an exception register with rationale; do not allow cosmetic variance to stall progress or mask true defects.

## Define protected namespaces before broad audits

Discovery and cleanup automation must respect explicit exclusion boundaries. Recovery bundles, backup archives, filesystem snapshots (`#snapshot`, `@eaDir`), and quarantine roots must never be traversed by general recursive sweeps unless explicitly scoped and authorized.

## Recreate and reboot are tests

A running service may still depend on stale runtime configuration. Recreate validates desired state; reboot validates schedulers, durable paths, restart policies, and hidden ordering assumptions.

## Capacity claims need filesystem context

Apparent size is not physical allocation. Hardlinks, snapshots, compression, sparse files, metadata, and delayed reclamation all affect observed free space. State what is being measured.

## Public artifacts should be rewritten

Operational reports contain an infrastructure fingerprint even when credentials are absent. A reusable public playbook should be derived from lessons and methods, never produced by bulk-redacting and uploading the report tree.
