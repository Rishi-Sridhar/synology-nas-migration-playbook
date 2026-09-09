# Filesystem and ACL Remediation

Synology permissions may combine POSIX mode bits, ownership, groups, inherited ACL entries, DSM share policy, and container UID/GID mappings. A directory that looks writable to an administrator may still fail for a container.

## Diagnose from the effective identity

Record the container's UID, GID, supplementary groups, mount options, and the host path behind the bind. Inspect every parent directory for traversal permission. Capture POSIX modes and Synology ACL output before changing anything.

Test read, create, rename, and delete separately using a disposable file and the service's effective identity. These operations require different permissions.

## Remediate narrowly

Prefer correcting ownership/group design and inherited ACL policy at the intended root. Avoid recursive world-writable modes. Before a recursive change, export the existing ACLs privately, measure the target count, exclude snapshots and unrelated trees, and rehearse on a small subtree.

After remediation:

- Re-run effective-identity tests.
- Confirm inherited entries on a newly created directory.
- Exercise the application's failed operation.
- Check that unrelated services did not gain broader access.
- Record the before/after policy, not private ACL dumps, in public documentation.
