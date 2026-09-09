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
<NAS_VOLUME>/media/movies
<NAS_VOLUME>/media/tv
<NAS_VOLUME>/downloads/qbit/movies
<NAS_VOLUME>/downloads/qbit/tv
<NAS_VOLUME>/docker/<service>
<NAS_VOLUME>/host-scripts/<automation>
<BACKUP_ROOT>/recovery/<component>
<LEGACY_STAGING_ROOT>  # temporary, preferably read-only
```

Container paths should be stable even if host volumes change. For example, map canonical host media roots to `/media/movies` and `/media/tv`, and download roots to `/downloads/...`. Keep the same container-side vocabulary across qBittorrent and ARR services where remote path mapping is not required.

## Evidence flow

```text
frozen inventory
  -> dependency graph
  -> decision ledger
  -> copy manifest
  -> byte/hash verification
  -> application rebinding
  -> live-state validation
  -> deletion manifest
  -> execution receipt
  -> closeout report
```

Every artifact has a narrow purpose. An inventory records facts; a decision ledger records human intent; a receipt records what actually happened. Do not let a script infer a deletion decision from a low playback count or a stale path.
