# Path Mapping Example

Keep the populated version private. Record both host and container paths because applications usually persist the latter.

| Purpose | Old host path | New host path | Container path | Consumers | State |
| --- | --- | --- | --- | --- | --- |
| Movies | `<OLD_MEDIA_ROOT>/movies` | `/volume1/media/movies` | `/media/movies` | Plex, Radarr | planned |
| TV | `<OLD_MEDIA_ROOT>/tv` | `/volume1/media/tv` | `/media/tv` | Plex, Sonarr | planned |
| Movie downloads | `<OLD_DOWNLOAD_ROOT>/movies` | `/volume1/downloads/qbit/movies` | `/downloads/qbit/movies` | qBittorrent, Radarr | planned |
| TV downloads | `<OLD_DOWNLOAD_ROOT>/tv` | `/volume1/downloads/qbit/tv` | `/downloads/qbit/tv` | qBittorrent, Sonarr | planned |
| Legacy keep set | `<STAGING_ROOT>/protected` | unchanged | `/legacy/protected` | qBittorrent | read-only exception |

For every row, add private evidence references for preflight inventory, copy verification, application rebinding, postcheck, rollback, and retirement eligibility.
