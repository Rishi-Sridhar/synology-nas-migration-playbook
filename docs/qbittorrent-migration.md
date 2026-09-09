# qBittorrent Migration

qBittorrent migration is a state migration, not merely a file copy. Preserve the relationship among torrent metadata, resume state, save path, content layout, and the bytes on disk.

## Safe sequence

1. Freeze changes: disable automatic management for the cohort and pause affected torrents.
2. Back up the qBittorrent profile privately. Never publish `BT_backup`, `.torrent`, or `.fastresume` files.
3. Record torrent identity, save path, content path, category, tags, completion, and piece count in a private manifest.
4. Copy payloads to the destination. Preserve names and relative layout exactly.
5. Verify bytes independently. Use full hashes for a small cohort; for large sets, combine size checks, sampled hashes, filesystem checks, and qBittorrent's force recheck.
6. Change the location using qBittorrent's supported UI or API. Do not hand-edit live resume files.
7. Force recheck and require 100% completion before resuming upload.
8. Confirm tracker state, errors, and actual disk reads from the new mount.
9. Retain the source until the observation window passes, then delete only from an approved manifest.

## Container path rule

The path understood by qBittorrent is its container path. Keep that path stable when feasible. If it must change, ensure the new host bind and the qBittorrent save path agree. A host directory existing does not prove it is visible inside the container.

## Failure gates

Stop if a torrent becomes missing-files, content layout changes, a destination collision exists, a hardlink relationship is misunderstood, or a private tracker requires an action outside its rules. Never announce or recreate torrent metadata casually; force recheck does not repair a wrong content root.
