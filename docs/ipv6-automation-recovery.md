# IPv6 Automation Recovery

Dynamic IPv6 prefixes can invalidate router firewall rules and service bindings after an address change. A resilient design reacts to network events, converges idempotently, and verifies the result externally.

## Generic design

```text
address event -> debounce -> compute desired address -> update local service
              -> update router rule -> update DNS -> external probe -> notify
```

Use the operating system's address-monitoring facility instead of a tight polling loop. Debounce bursts and serialize executions with a lock. The worker should be safe to run twice and should not log credentials or authenticated URLs.

## Recovery requirements

- Durable scripts outside ephemeral container layers
- A boot-time task that starts the watcher after networking is available
- Browser or API automation pinned to tested versions when a router lacks a stable API
- Credentials supplied at runtime from protected storage
- Timeouts, bounded retries, and screenshots/logs scrubbed of private data
- An external IPv6 reachability check, not only a local socket check

## Validation

Trigger a controlled address change or use a non-destructive test mode. Prove event detection, service rebinding, router update, DNS convergence, and external reachability. Reboot once and verify the scheduler, processes, and state lock recover cleanly.

Router UI automation is fragile. Keep selectors and credentials private, preserve a manual recovery path, and treat a vendor firmware update as a reason to rerun the controlled test.
