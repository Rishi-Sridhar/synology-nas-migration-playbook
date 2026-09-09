# Scripts

These helpers use only the Python standard library and are read-only by default.

## Verify a copied tree

```bash
python scripts/verify_copy.py <SOURCE_DIR> <DESTINATION_DIR> --hash sha256
```

The command compares relative paths, regular-file sizes, and optionally content hashes. It never deletes or modifies files.

## Audit a path map

```bash
python scripts/audit_path_mappings.py <MAPPINGS.csv>
```

Required CSV columns are `purpose`, `old_path`, `new_path`, and `container_path`. The helper rejects placeholders, duplicate destinations, relative paths, and overlapping new roots that could make a migration ambiguous.

Run these tools against a private manifest. Do not commit generated inventories or results from a live system.
