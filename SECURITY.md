# Security Policy

## Reporting a problem

Open a GitHub security advisory for vulnerabilities in the example scripts. Do not put credentials, private infrastructure details, torrent identifiers, or exploit data in a public issue.

## Data-handling rules

This repository must never contain:

- Live environment files, credentials, cookies, access tokens, or private keys
- qBittorrent state, torrent files, info hashes, or tracker-specific URLs
- Application databases or exports from Plex, Sonarr, Radarr, Prowlarr, or similar services
- Backup archives, recovery keys, Docker image exports, or raw operational reports
- Personal hostnames, domains, usernames, IP addresses, or media inventories

Use placeholders in committed examples. Store deployment values in ignored local files with least-privilege permissions. Rotate any credential that is accidentally committed; deleting it in a later commit is insufficient because Git history retains it.

## Operational safety

Run discovery and validation with read-only credentials where possible. Separate planning, execution, and verification. Require an explicit manifest for deletion, bind it to a fresh observation, and fail closed if live state differs.
