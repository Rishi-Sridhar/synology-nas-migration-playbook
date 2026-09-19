# Path Mapping Example

Keep the populated version private. Record both host and container paths because applications usually persist the latter.

| Purpose | Old host path | New host path | Container path | Consumers | Migration state | Lifecycle state |
| --- | --- | --- | --- | --- | --- | --- |
| Movies | `<OLD_MEDIA_ROOT>/movies` | `/srv/storage/active/media/movies` | `/media/movies` | Plex, Radarr | completed | active |
| TV | `<OLD_MEDIA_ROOT>/tv` | `/srv/storage/active/media/tv` | `/media/tv` | Plex, Sonarr | completed | active |
| Movie downloads | `<OLD_DOWNLOAD_ROOT>/movies` | `/srv/storage/active/downloads/qbit/movies` | `/downloads/qbit/movies` | qBittorrent, Radarr | completed | active |
| TV downloads | `<OLD_DOWNLOAD_ROOT>/tv` | `/srv/storage/active/downloads/qbit/tv` | `/downloads/qbit/tv` | qBittorrent, Sonarr | completed | active |
| Legacy staging cohort A | `<STAGING_ROOT>/cohort-a` | `/srv/storage/quarantine/cohort-a` | unmounted | none | cutover complete | quarantined |
| Legacy staging cohort B | `<STAGING_ROOT>/cohort-b` | `/srv/storage/quarantine/cohort-b` | unmounted | none | soak complete | deletion-eligible |
| Legacy staging cohort C | `<STAGING_ROOT>/cohort-c` | purged | unmounted | none | retired | purged |
| Legacy keep set | `<STAGING_ROOT>/protected` | unchanged | `/legacy/protected` | qBittorrent | exception | active (read-only) |

For every row, add private evidence references for preflight inventory, copy verification, application rebinding, postcheck, rollback, quarantine isolation, soak observation, and retirement eligibility.
