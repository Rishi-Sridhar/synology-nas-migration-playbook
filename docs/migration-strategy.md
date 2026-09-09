# Migration Strategy

## Phase 0: define invariants

Write down what must remain true: active downloads are not interrupted unexpectedly, seeded payloads remain verifiable, media paths resolve, service databases persist, and named exceptions remain untouched. Define capacity targets and minimum free-space floors in bytes.

## Phase 1: discover

Collect read-only snapshots of:

- Mounts, volumes, shares, filesystem types, free space, snapshots, and quotas
- File identity `(device, inode)`, link count, apparent size, and allocated size
- qBittorrent torrent state, save paths, categories, tags, and content layout
- ARR root folders, download clients, remote path maps, queues, and health
- Docker containers, mounts, networks, volumes, Compose labels, and health
- DSM scheduled tasks, ACLs, and recovery locations

Timestamp the snapshot and record tool versions. Unknowns are blockers, not invitations to guess.

## Phase 2: model dependencies

Build a path map and a graph from files to consumers. A pathname may be referenced by qBittorrent, Plex, an ARR database, a container bind, a script, or a backup job. Hardlinked pathnames share one physical inode and must be handled as a unit for storage accounting.

## Phase 3: migrate a canary

Choose a small, reversible cohort. Pause only the affected workload, copy without deleting, verify size and hashes, update bindings, force application rechecks, and observe through a full service cycle. Record the exact rollback action.

## Phase 4: expand in cohorts

Use immutable manifests. Before each mutation, re-stat sources and compare them with the manifest to prevent time-of-check/time-of-use drift. Stop on missing files, changed sizes, unexpected links, active transfers, or insufficient destination space.

## Phase 5: retire selectively

Classify the old tree into `DELETE`, `KEEP`, and `UNKNOWN`. Only `DELETE` enters an execution manifest. Mount retained legacy paths read-only when possible. Never use a broad recursive deletion as a substitute for classification.

## Phase 6: close out

Validate from the filesystem, each application, and the recovery path. Preserve intentional exceptions as first-class documentation. A migration can close with exceptions; it cannot close with unexplained drift.
