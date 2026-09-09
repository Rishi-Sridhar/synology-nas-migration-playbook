# Disaster Recovery

A migration backup is useful only if it is complete, restorable, and independent of the system being migrated.

## Recovery bundle contents

For each critical component, privately preserve:

- Versioned configuration and Compose specifications
- Application-consistent database backups
- Durable host scripts and scheduler definitions
- Image references or reproducible build instructions
- Environment-variable names plus a separate protected secret source
- Restore order, prerequisites, health checks, and rollback steps
- Checksums and a manifest of the bundle

Do not place credentials inside the documentation archive merely for convenience. Keep key custody separate from encrypted backup storage.

## Three-copy mindset

Maintain a production copy, a local recovery copy on a different failure domain, and an offsite encrypted copy. NAS snapshots help with quick rollback but do not protect against device loss, account compromise, or every form of corruption.

## Restore drill

At least once, restore into an isolated directory or disposable host. Verify archive integrity, secret injection, container creation, database opening, scheduled-task recreation, and an end-to-end health check. Record the tested version and date.

Back up the evidence needed to rebuild, not every transient cache or exported image by default. If a large binary is included, justify why it cannot be reproduced and monitor its lifecycle for vulnerabilities.
