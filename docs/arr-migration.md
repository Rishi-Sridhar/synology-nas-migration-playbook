# Sonarr and Radarr Migration

ARR applications store paths in several places: root folders, series or movie records, download-client settings, queue entries, import lists, and sometimes remote path mappings. Fixing only one surface leaves path debt.

## Target model

- qBittorrent categories route future downloads into explicit subdirectories.
- Sonarr and Radarr see the same container-side download paths as qBittorrent when co-located.
- Media libraries have canonical roots separate from active download roots.
- Completed-download handling imports through atomic moves or hardlinks only when source and destination share a filesystem.

## Remediation sequence

1. Back up each application database privately and stop writers if taking a direct database snapshot.
2. Inventory root folders, item paths, download-client categories, remote mappings, queues, and health messages.
3. Define old-to-new path mappings and reject overlapping or ambiguous rules.
4. Change root folders through the application when possible. Move or reassign items in small cohorts.
5. Align container binds before testing imports.
6. Test one download through grab, completion, import, rename, rescan, and playback.
7. Query for stale path prefixes and require a count of zero, except documented rollback entries.
8. Confirm permissions by creating and removing a disposable file as the container's effective UID/GID.

## Avoid silent database surgery

Direct SQLite changes can bypass invariants and should be a last resort. If required, stop the application, take a consistent backup, document every statement, constrain updates by exact old prefixes, check affected-row counts, run database integrity checks, and start with a rollback rehearsal.
