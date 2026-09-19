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
4. Verify mount exposure: confirming that the directory exists on the host is not enough. Verify that:
   - The intended container receives the path at the correct internal mount point.
   - The application configuration references the internal path.
   - The container's effective UID/GID has read, write, and traverse permissions.
5. Change root folders through the application's native UI or REST API. Move or reassign items in small cohorts.
6. Align container binds before testing imports.
7. Test one download through grab, completion, import, rename, rescan, and playback.
8. Query for stale path prefixes and require a count of zero, except documented rollback entries.
9. Confirm permissions by creating and removing a disposable file as the container's effective UID/GID.

## SQLite WAL mode and database safety

ARR applications use SQLite databases frequently configured in Write-Ahead Logging (WAL) mode (`-wal` and `-shm` companion files). Observe these safety boundaries:

- **Avoid host-side inspection of live databases**: Do not run host-level `sqlite3`, Python scripts, or external backup queries against a live SQLite database while the application container is running. External concurrent access can lead to file locking conflicts, dirty reads, or schema corruption.
- **Never perform direct live modifications**: Direct SQL updates bypass application caches, internal validation logic, and event queues.
- **Prefer official APIs**: Use the application's documented REST API or UI for all path updates, library resynchronization, and queue management.
- **Clean state for maintenance**: If direct database inspection or emergency repair is unavoidable, cleanly stop the container first. Ensure all WAL entries are checkpointed into the main database file, create an immutable backup, document every statement, and rehearse the rollback procedure before touching data.
