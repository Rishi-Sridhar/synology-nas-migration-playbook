# Validation and Closeout

Closeout is an independent audit of the current system, not a summary of commands that previously returned success.

## Validation matrix

| Domain | Minimum evidence |
| --- | --- |
| Filesystem | Expected roots exist; counts and bytes reconcile; no unexpected legacy paths |
| qBittorrent | Census reconciles; no missing files; selected torrents recheck at 100% |
| Cross-seed | Registrations and shared payload topology reconcile; removal did not delete media |
| Sonarr/Radarr | Root paths, queues, health, imports, renames, and stale-prefix queries pass; no live SQLite WAL external query violations |
| Docker | Desired and runtime mounts match via `docker inspect`; container-internal paths verified; services healthy; mutation streams remained narrow |
| ACLs | Effective service identity can perform required operations and no more |
| Quarantine | Legacy roots isolated from service paths; replacement paths healthy and verified |
| Soak | At least one complete operational cycle of background tasks, automated grabs, and backups completes without errors or references to legacy root |
| Reference absence | Bounded audit verifies zero active references to old roots across Compose specs, runtime mounts, scheduled jobs, and application databases |
| Rollback | Rollback manifests, database dumps, and recovery bundles preserved intact through closeout |
| DR | Bundle checksum and isolated restore drill pass |

## Evidence classification

Before closing a migration cohort, classify all findings:

- **Correctness failure** (`FAIL`): Data divergence, missing files, hash mismatches, broken mounts, or permission errors. These are blockers that must be resolved before proceeding.
- **Evidence blemish** (`PASS_WITH_EXCEPTION`): Benign variances (such as timestamp drift, regenerated cache files, or log formatting changes) that do not compromise data integrity or operational correctness. Each accepted blemish must be documented in the exceptions register with root-cause rationale.

## Closeout artifacts

Produce a sanitized executive report, a machine-readable final state, an intentional-exceptions register, recovery pointers, and an index of private evidence. Keep raw reports private.

Use explicit results such as `PASS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`. Every `PASS` should cite a timestamped observation. A tolerated condition belongs in the exceptions register with its owner, risk, and retirement trigger.

## Final gate

Close only when:
1. Migration validation passes across all active services.
2. Rollback or recovery assets are verified viable and preserved intact.
3. Live observations show zero regression during the soak observation period.
4. Remaining operational work is explicitly optional.

Passing migration validation establishes operational readiness. It does not constitute authorization for permanent deletion: permanent purging of quarantined data remains a separate, explicitly authorized destructive procedure. Re-run a privacy and credential scan before sharing any closeout material.
