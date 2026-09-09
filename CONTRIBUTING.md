# Contributing

Contributions should make the playbook safer, clearer, or more reusable.

Before opening a pull request:

1. Use only invented examples and placeholders.
2. Do not attach logs, screenshots, databases, torrent metadata, or configuration copied from a live system.
3. Run the Python helpers with `--help` and test changes against temporary sample directories.
4. Search the staged diff for credentials, personal paths, hostnames, IP addresses, hashes, and tracker identifiers.
5. Explain the failure mode addressed and the validation evidence expected.

Prefer standard-library scripts and commands that are read-only by default. Destructive examples must include a dry-run mode, an explicit scope, and a postcondition check.
