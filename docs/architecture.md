# Architecture

## Separate planes

A reliable migration keeps four concerns distinct:

1. **Data plane** — media, download payloads, application data, and backups.
2. **Path plane** — host paths, container mounts, and paths stored inside application databases.
3. **Control plane** — Compose projects, DSM tasks, health checks, and network automation.
4. **Evidence plane** — inventories, manifests, hashes, receipts, exceptions, and closeout reports.

Confusing these planes causes common failures. Moving a file changes the data plane; it does not update a torrent save path or an ARR root. Recreating a container updates the control plane; it does not prove its database survived.

## Generic target layout

```text
/srv/storage/active/media/movies
/srv/storage/active/media/tv
/srv/storage/active/downloads/qbit/movies
/srv/storage/active/downloads/qbit/tv
/srv/storage/active/docker/<service>
/srv/storage/quarantine/<cohort-timestamp>/
/srv/storage/archive/<backup-bundle>/
<HOST_SCRIPTS_ROOT>/<automation>
```

Container paths should be stable even if host roots change. For example, map canonical active media roots to `/media/movies` and `/media/tv`, and download roots to `/downloads/...`. Keep the same container-side vocabulary across qBittorrent and ARR services where remote path mapping is not required.

## Path existence is not active exposure

A directory existing on the host does not mean it is actively in use or correctly exposed. Active exposure must be verified independently across:

- **Configured mounts**: Declarations in Compose files or service unit definitions.
- **Runtime container mounts**: Inspected live mount binds (`docker inspect`) verifying host path, container-internal destination, and read/write flags.
- **Scheduled tasks and automation**: Cron jobs, systemd timers, or host scheduler scripts referencing the path.
- **Application configuration**: Internal database roots, library folders, and download client save paths.

Conversely, an unreferenced path on disk is not proof that no container expects it. Verify both directions before changing or retiring any path.

## Evidence flow

```text
frozen inventory
  -> dependency graph
  -> decision ledger
  -> copy manifest
  -> byte/hash verification
  -> application rebinding
  -> live-state validation
  -> quarantine old root
  -> soak observation
  -> deletion eligibility review
  -> explicit destructive authorization
  -> execution receipt
  -> closeout report
```

Every artifact has a narrow purpose. An inventory records facts; a decision ledger records human intent; a receipt records what actually happened. Do not let a script infer a deletion decision from a low playback count or a stale path.

## Protected namespaces

Certain namespaces must be treated as structurally protected from broad automated audits and bulk cleanup:

- **Recovery bundles and archives**: Durable backups, exported configurations, and disaster-recovery bundles.
- **Quarantine roots**: Staged data undergoing soak observation.
- **Filesystem snapshot trees**: Storage snapshots (such as `#snapshot` or `@eaDir` metadata) that must not be traversed or altered by general tools.
- **Operator-declared exclusions**: Explicit directories designated as intentional exceptions.

Automated discovery, validation, or cleanup tools must not recursively traverse protected namespaces unless that exact namespace is explicitly scoped and authorized for inspection.
