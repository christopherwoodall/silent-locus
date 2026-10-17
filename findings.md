# Platform Limitations — Findings (2026-10-17)

Determined by a four-lane counsel convened at BigSexyWarlock69's order.
Decision: accept and work around (not escalate).

## 1. The exec sandbox write throttle

File writes issued through the shell on this VM intermittently fail with
`PermissionError: [Errno 1] Operation not permitted`, in waves lasting
minutes, then clear on their own.

This is **not a disk fault**. It is the platform protecting itself under
pressure: a dynamic, time-varying throttle on the exec sandbox's write path.

### What was proven

- The failing call is `write()` — `open()` succeeds (the file is created,
  zero bytes), then the first data write is denied. Same for `writev`,
  `pwrite64`, `copy_file_range`.
- Only regular-file data writes are blocked. `mkdir`, `rename`, `chmod`,
  `unlink`, reads, pipes, and sockets all work during a wave.
- The decision flickers per-syscall: the same binary gets opposite outcomes
  seconds apart. A static filter cannot do this.
- The tool path (`muse.write` / `muse.edit`) **never** fails. A real
  filesystem fault would strike it equally. The throttle lives on the exec
  path only.

### What was ruled out

Overlayfs bug, inode/space exhaustion, AppArmor/SELinux, disk quota,
hypervisor fault, OOM side effects, writeback storms — each killed by
evidence (wrong errno, wrong scope, or the tool-path test).

### What trips it

System pressure — specifically ours. At the time of measurement: CPU
saturated, memory at 11.6% available with no swap, 17–28 concurrent factum
writer processes hammering a 1 GB SQLite database. The throttle engages to
keep the box alive.

## 2. What this limits

- **git**: cannot write objects during a wave (`fatal: unable to write loose
  object file`). Commits and pushes must ride out the wave — retry with
  backoff, do not fight it.
- **Shell file writes**: `cp`, redirects, and script output fail
  intermittently during waves. Single isolated writes usually succeed;
  bursts fail.
- **Anything that must land**: route through the tool path, which is
  unaffected.

## 3. Workarounds (standing)

1. Reduce the pressure that trips the throttle. The factum write-path fix
   (2026-10-17) cuts per-write compute ~5x; serializing writers to a FIFO
   queue cuts 17–28 concurrent writers to one.
2. Route must-land writes through `muse.write` / `muse.edit`.
3. For git: retry loop with backoff until the wave clears, then verify
   remote HEAD == local HEAD. For the standalone factum repo, push via the
   GitHub API (`push.py`), which needs no local git objects.
4. Watch memory: no swap, and one OOM kill has already happened. Fewer
   concurrent writers is the mitigation available from inside.

## 4. What cannot be fixed from inside

The throttle itself is runtime policy. Its exact owner is not visible from
this container, and `dmesg` is restricted. Tuning or raising it needs the
platform, not us. The counsel's recommendation — accepted — is to treat it
as a fact of life: our load was the trigger, and the fix already in flight
removes that load.
