# Validation and Closeout

Closeout is an independent audit of the current system, not a summary of commands that previously returned success.

## Validation matrix

| Domain | Minimum evidence |
| --- | --- |
| Filesystem | Expected roots exist; counts and bytes reconcile; no unexpected legacy paths |
| qBittorrent | Census reconciles; no missing files; selected torrents recheck at 100% |
| Cross-seed | Registrations and shared payload topology reconcile; removal did not delete media |
| Sonarr/Radarr | Root paths, queues, health, imports, renames, and stale-prefix queries pass |
| Docker | Desired and runtime mounts match; services are healthy; state persists after recreate |
| ACLs | Effective service identity can perform required operations and no more |
| Staging | Delete/keep/unknown coverage is complete; protected sets remain; unexpected files are zero |
| Automation | Boot start, event trigger, convergence, external probe, and notification pass |
| DR | Bundle checksum and isolated restore drill pass |

## Closeout artifacts

Produce a sanitized executive report, a machine-readable final state, an intentional-exceptions register, recovery pointers, and an index of private evidence. Keep raw reports private.

Use explicit results such as `PASS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`. Every `PASS` should cite a timestamped observation. A tolerated condition belongs in the exceptions register with its owner, risk, and retirement trigger.

## Final gate

Close only when all destructive manifests have receipts, live observations show no regression, rollback or recovery is viable, and remaining work is explicitly optional. Re-run a privacy and credential scan before sharing any closeout material.
