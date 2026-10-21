#!/usr/bin/env python3
"""
Linux Privilege Escalation Enumerator
Propietary Software. ONLY USE IN YOUR OWN DEVICES.
I DO NOT CLAIM RESPONSIBILITY OF MISUSE.
"""

import os
import subprocess
import stat
import pwd
import grp

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
    except:
        return ""

def section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

# ── Current User Context ──────────────────────────
section("CURRENT USER CONTEXT")
print(run("id"))
print(run("whoami"))
print(run("hostname"))

# ── Sudo Permissions ──────────────────────────────
section("SUDO PERMISSIONS")
print(run("sudo -l 2>/dev/null"))

# ── SUID Binaries ─────────────────────────────────
section("SUID BINARIES (cross-ref GTFOBins)")
suid = run("find / -perm -4000 -type f 2>/dev/null")
print(suid)

# ── Writable /etc/passwd ──────────────────────────
section("WRITABLE SENSITIVE FILES")
sensitive = ["/etc/passwd", "/etc/shadow", "/etc/sudoers"]
for f in sensitive:
    if os.path.exists(f) and os.access(f, os.W_OK):
        print(f"[!!!] WRITABLE: {f}")

# ── Cron Jobs ─────────────────────────────────────
section("CRON JOBS")
print(run("cat /etc/crontab"))
print(run("ls -la /etc/cron.*"))

# ── Writable Cron Scripts ─────────────────────────
section("WRITABLE SCRIPTS IN CRON")
cron_dirs = ["/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly"]
for d in cron_dirs:
    if os.path.exists(d):
        for f in os.listdir(d):
            full = os.path.join(d, f)
            if os.access(full, os.W_OK):
                print(f"[!!!] WRITABLE CRON SCRIPT: {full}")

# ── PATH Hijacking Check ──────────────────────────
section("PATH HIJACKING — WRITABLE DIRS IN $PATH")
path_dirs = os.environ.get("PATH", "").split(":")
for d in path_dirs:
    if os.path.exists(d) and os.access(d, os.W_OK):
        print(f"[!!!] WRITABLE PATH DIR: {d}")

# ── Capabilities ──────────────────────────────────
section("BINARY CAPABILITIES")
print(run("getcap -r / 2>/dev/null"))

# ── Interesting Files ─────────────────────────────
section("INTERESTING FILES (SSH keys, history, configs)")
interesting = [
    "~/.ssh/id_rsa", "~/.bash_history", "~/.zsh_history",
    "/root/.bash_history", "~/.aws/credentials"
]
for f in interesting:
    expanded = os.path.expanduser(f)
    if os.path.exists(expanded) and os.access(expanded, os.R_OK):
        print(f"[+] READABLE: {expanded}")

# ── World-Writable Directories ────────────────────
section("WORLD-WRITABLE DIRECTORIES")
print(run("find / -type d -perm -0002 2>/dev/null | grep -v proc"))

# ── Kernel Version ────────────────────────────────
section("KERNEL VERSION (check against known exploits)")
print(run("uname -a"))
print(run("cat /etc/os-release"))

# ── Running Processes / Services ──────────────────
section("INTERESTING RUNNING PROCESSES")
print(run("ps aux --no-headers | grep -v '\[' | awk '{print $1, $11}'"))

# ── Network Listeners ─────────────────────────────
section("LOCAL NETWORK LISTENERS")
print(run("ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null"))

print("\n[✓] Enumeration complete. Cross-reference SUID results with GTFOBins.xyz\n")
