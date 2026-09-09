# Lessons Learned

## Evidence beats intuition

Storage names, media titles, and application labels are hints, not identities. Filesystem identity, content verification, application state, and fresh observations prevent confident but unsafe decisions.

## Separate registration from payload deletion

Removing a torrent registration and deleting its files are different operations. Keeping them separate is especially important for cross-seeds, hardlinks, and library-resident media.

## Canonical paths reduce future debt

Stable container paths and explicit download categories make host-volume changes less disruptive. After remediation, query every state surface for old prefixes; do not stop after editing the visible root folder.

## Preserve small ambiguities

Deleting tiny unknown Docker volumes or zero-reclaim hardlink names offers little benefit and disproportionate regression risk. An intentional exception is often the correct engineering result.

## Recreate and reboot are tests

A running service may still depend on stale runtime configuration. Recreate validates desired state; reboot validates schedulers, durable paths, restart policies, and hidden ordering assumptions.

## Capacity claims need filesystem context

Apparent size is not physical allocation. Hardlinks, snapshots, compression, sparse files, metadata, and delayed reclamation all affect observed free space. State what is being measured.

## Public artifacts should be rewritten

Operational reports contain an infrastructure fingerprint even when credentials are absent. A reusable public playbook should be derived from lessons and methods, never produced by bulk-redacting and uploading the report tree.
