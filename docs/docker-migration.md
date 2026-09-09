# Docker Compose Migration

Treat a container as reproducible configuration plus persistent state. `docker inspect` describes runtime truth; a Compose file describes desired truth. Capture both before migration.

## Inventory

Record image digests, commands, environment variable names (not values), bind mounts, named volumes, networks, ports, health checks, restart policies, device mappings, capabilities, and Compose labels. Classify every mount as configuration, database/state, cache, media, download, or socket/device.

## Safe relocation

1. Copy persistent data while the service is stopped or use an application-consistent backup.
2. Put host paths under a canonical root such as `<NAS_VOLUME>/docker/<service>`.
3. Keep confidential values in an ignored `.env` or secret store with restrictive permissions.
4. Render the resolved specification with `docker compose config` and review it without publishing the output; interpolation may expose values.
5. Recreate, do not merely restart, containers whose mounts or environment changed.
6. Compare the new `docker inspect` result with the intended specification.
7. Validate health, logs, persistence, and dependent-service connectivity.

## Housekeeping

Do not equate `unused` with `safe to delete`. Before removing an image, volume, or network, prove that no running or stopped container, rollback plan, or recovery procedure depends on it. Small ambiguous volumes are usually cheaper to retain than to misclassify.

Use [the example Compose file](../examples/docker-compose.example.yml) only as a structure guide. Pin tested image versions or digests in real deployments.
