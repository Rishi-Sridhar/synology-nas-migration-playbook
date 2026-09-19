# Staging Retirement

A legacy staging root often contains a mixture of obsolete copies, live torrent payloads, rollback data, and application-visible paths. Retire it by staged manifest and quarantine, not by immediate directory deletion.

## Classification

Assign every leaf in the staging inventory to one state:

- `DELETE` — proven redundant and unreferenced; marks candidate as **eligible for retirement workflow** (never immediate deletion)
- `KEEP` — an active dependency or explicit rollback asset
- `UNKNOWN` — incomplete evidence; automatically protected

The default is `UNKNOWN`. Require coverage accounting so the sum of classified files equals the fresh, bounded filesystem inventory. Do not recurse into declared protected namespaces (such as recovery bundles, backup trees, or snapshot directories).

## Retirement lifecycle

```text
candidate
  -> classified
  -> quarantined
  -> soaked
  -> deletion-eligible
  -> explicitly authorized
  -> purged
```

### 1. Quarantine (reversible isolation)

Before quarantining:
- Verify replacement data exists and hashes/sizes match on the active root.
- Confirm active service containers use the new host and container paths.
- Verify rollback archives and manifests remain intact.
- Capture an immutable, bounded manifest of the files entering quarantine.

Quarantine must be reversible: move the cohort into a dedicated quarantine root (e.g., `/srv/storage/quarantine/<cohort-timestamp>/`), adjust mount permissions, or remove container bind exposure.

### 2. Soak observation

Enforce a soak window while the quarantined files remain fully recoverable. The soak period must span at least one complete operational cycle of background tasks, automated grabs, scheduled library rescans, and backup jobs. Any service error, missing file warning, or unexpected attempt to access the quarantined path halts the retirement workflow and triggers investigation.

### 3. Deletion eligibility and reference absence

Before a quarantined cohort can be deemed deletion-eligible, verify zero active references through bounded inspection of:
- Current Docker Compose specifications.
- Live runtime container inspect outputs (`docker inspect`).
- Host scheduled tasks, cron jobs, and maintenance scripts.
- Application configuration files and internal databases.
- Host symlinks or bind mounts pointing to the legacy path.

### 4. Execution gates and authorization

```text
PASSING ALL GATES ESTABLISHES DELETION ELIGIBILITY.
IT DOES NOT ITSELF CONSTITUTE DELETE AUTHORIZATION.
```

Permanent purge must remain an explicit destructive operator action executed against an approved manifest:

1. Re-stat each target file immediately prior to unlinking to prevent time-of-check/time-of-use drift.
2. Confirm no active processes hold open file handles in the target directory.
3. Run a dry pass that outputs exact target counts and bytes.
4. Execute exact file unlinks per manifest (never use broad recursive `rm -rf`).
5. Record one execution receipt per unlinked file.
6. Stop immediately on the first error or unexpected file condition.
7. Remove parent empty directories only after a subsequent inventory confirms emptiness.

## Afterward

Mount any required legacy compatibility bind read-only. Confirm all active consumers continue to operate normally. Compare expected and observed file counts and bytes, and verify physical storage reclamation; snapshots, hardlinks, and filesystem metadata can cause observed free space to differ from apparent unlinked bytes.
