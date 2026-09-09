# Cross-Seed Safety

Cross-seeding means multiple torrent registrations may reference the same payload. The registrations are logically separate even when the bytes, pathnames, or inodes overlap.

## Build the topology first

For each private torrent record, map:

```text
<TORRENT_HASH> -> <TRACKER> -> save path -> content root -> file set -> (device,inode)
```

Group torrents by content identity, not title. Names and sizes alone are insufficient. Compare relative paths and file sizes, then verify strong hashes or piece data where practical.

## Hardlinks change deletion math

Two pathnames with the same `(device, inode)` do not consume two copies of the file's blocks. Removing one name normally reclaims no blocks while another hardlink remains. Report both apparent bytes and estimated physical reclaim; never sum pathname sizes as reclaimable capacity.

Hardlinks do not cross filesystems. A copy to another volume creates new inodes even if a tool describes the operation as preserving links within each side.

## Safe removal rule

Removing a dead registration should normally use `deleteFiles=false` until every peer registration and media consumer has been checked. Deleting payload data is a separate decision with a separate manifest.

Before deleting any pathname, prove that:

- It is not the sole path used by an active torrent.
- It is not the path imported into a media library.
- Its current inode/link count matches the recorded evidence.
- The expected physical reclaim is understood.
- The action complies with tracker rules.

Cross-seed software should preserve category semantics. If duplicate categories are enabled, document which category owns automation and which categories are only labels so ARR does not import the same payload twice.
