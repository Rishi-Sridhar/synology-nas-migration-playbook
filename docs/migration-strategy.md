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

Choose a small, reversible cohort. Keep the mutation stream strictly narrow:
- Mutate and rebind only the current cohort.
- Restart or recreate only affected services.
- Never restart the entire Docker daemon or unrelated service stacks without an explicit operational reason.

Pause only the affected workload, copy without deleting, verify size and hashes, update bindings, validate mount visibility, force application rechecks, and observe through a full service cycle. Record the exact rollback action and preserve rollback assets.

## Phase 4: expand in cohorts

Use immutable manifests and maintain narrow mutation streams throughout cohort expansion. Before each mutation, re-stat sources and compare them with the manifest to prevent time-of-check/time-of-use drift. Stop on missing files, changed sizes, unexpected links, active transfers, or insufficient destination space.

Exclude declared protected namespaces (such as recovery bundles, backup trees, and quarantine roots) from general automated scans.

## Phase 5: quarantine and retire selectively

Do not treat successful migration cutover as immediate authorization for deletion. Retirement follows an explicit, staged safety lifecycle:

```text
validated migration
  -> quarantine
  -> soak observation
  -> deletion eligibility review
  -> explicit destructive authorization
  -> purge
```

1. **Classify**: Assign old paths to `DELETE`, `KEEP`, and `UNKNOWN`. In this model, `DELETE` designates *eligible for retirement workflow*, never immediate destruction.
2. **Quarantine**: Reversibly isolate the legacy root from service paths (for example, move to a quarantine directory, revoke container read access, or unbind).
3. **Soak**: Enforce an observation window while legacy data remains recoverable. Soak durations should scale to the workload's scheduled activity and operational risk (for example, 24–72 hours is typical for frequent home-lab cycles, but is illustrative rather than universal). The essential requirement is that at least one meaningful cycle of all relevant scheduled/background tasks (such as library updates, automated searches, or backups) completes without error or unexpected references to the legacy root.
4. **Prove absence**: Confirm zero active references across Compose mounts, runtime containers, scheduled jobs, and application databases before any destructive step.
5. **Authorize and purge**: Passing all checks establishes deletion eligibility. Permanent unlinking requires an explicit, separate destructive authorization and must never use broad recursive deletion.

## Phase 6: close out

Validate independently from the filesystem, each application, and the recovery path:

- **Preserve rollback assets**: Retain rollback manifests, recovery bundles, database snapshots, and prior known-good configs intact until formal closeout sign-off.
- **Evidence classification**: Distinguish between:
  - **Correctness failure**: Blockers requiring immediate resolution (for example: missing bytes, hash mismatches, missing container mounts, permission errors, broken bindings, or unexpected data alterations).
  - **Non-blocking evidence blemish**: Documented, benign variances that do not impair data or service integrity (for example: harmless timestamp variations, regenerated cache files, or log formatting changes). Blemishes must be explicitly justified in the exception register, not silently overlooked.
- **Exceptions register**: A migration can close with documented, intentional exceptions; it cannot close with unexplained drift.
