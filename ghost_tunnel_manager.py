"""
GhostCore Ghost Tunnel Manager
================================
Manages the lifecycle of the Ghost Tunnel Go proxy binary.
Launches ghost_tunnel.exe with OS-specific TLS/TCP profiles
and returns the local port for Chromium to connect through.
"""

import os
import sys
import subprocess
import time
import threading
import signal

# Path to the compiled Go binary
GHOST_TUNNEL_EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ghost_tunnel', 'ghost_tunnel.exe')

# OS → TLS Profile mapping
OS_TLS_PROFILES = {
    'Windows 11':       {'tls': 'chrome_windows', 'ttl': 128},
    'Windows 10':       {'tls': 'chrome_windows', 'ttl': 128},
    'macOS Sonoma':     {'tls': 'chrome_macos',   'ttl': 64},
    'macOS Ventura':    {'tls': 'chrome_macos',   'ttl': 64},
    'macOS Monterey':   {'tls': 'chrome_macos',   'ttl': 64},
    'Ubuntu 24.04 LTS': {'tls': 'chrome_linux',   'ttl': 64},
    'Fedora 40':        {'tls': 'chrome_linux',   'ttl': 64},
    'iOS':              {'tls': 'ios_safari',      'ttl': 64},
    'Android':          {'tls': 'android_chrome',  'ttl': 64},
}


class GhostTunnel:
    """
    Manages a single Ghost Tunnel proxy instance for one browser profile.
    """

    def __init__(self, profile_os='Windows 11', upstream_type='direct',
                 upstream_addr='', upstream_user='', upstream_pass=''):
        self.profile_os = profile_os
        self.upstream_type = upstream_type
        self.upstream_addr = upstream_addr
        self.upstream_user = upstream_user
        self.upstream_pass = upstream_pass
        self.process = None
        self.local_port = 0
        self._reader_thread = None

    def start(self):
        """Launch ghost_tunnel.exe and return the local listening port."""
        if not os.path.exists(GHOST_TUNNEL_EXE):
            print(f"[Ghost Tunnel] WARNING: Binary not found at {GHOST_TUNNEL_EXE}, skipping tunnel.")
            return 0

        # Resolve TLS profile and TTL from OS name
        profile_cfg = OS_TLS_PROFILES.get(self.profile_os, {'tls': 'chrome_windows', 'ttl': 128})
        tls_profile = profile_cfg['tls']
        ttl = profile_cfg['ttl']

        # Build command line
        cmd = [
            GHOST_TUNNEL_EXE,
            f'--port=0',
            f'--tls-profile={tls_profile}',
            f'--ttl={ttl}',
            f'--upstream-type={self.upstream_type}',
        ]

        if self.upstream_addr:
            cmd.append(f'--upstream-addr={self.upstream_addr}')
        if self.upstream_user:
            cmd.append(f'--upstream-user={self.upstream_user}')
        if self.upstream_pass:
            cmd.append(f'--upstream-pass={self.upstream_pass}')

        print(f"[Ghost Tunnel] Starting: {' '.join(cmd)}", flush=True)

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
        except Exception as e:
            print(f"[Ghost Tunnel] ERROR: Failed to launch: {e}", flush=True)
            return 0

        # Read the magic "LISTENING:<port>" line from stdout
        try:
            line = self.process.stdout.readline().decode('utf-8', errors='replace').strip()
            if line.startswith('LISTENING:'):
                self.local_port = int(line.split(':')[1])
                print(f"[Ghost Tunnel] Active on 127.0.0.1:{self.local_port} "
                      f"(TLS={tls_profile}, TTL={ttl}, upstream={self.upstream_type})", flush=True)
            else:
                print(f"[Ghost Tunnel] WARNING: Unexpected startup output: {line}", flush=True)
                self.stop()
                return 0
        except Exception as e:
            print(f"[Ghost Tunnel] ERROR: Failed to read port: {e}", flush=True)
            self.stop()
            return 0

        # Background thread to consume stderr logs
        self._reader_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._reader_thread.start()

        return self.local_port

    def _read_stderr(self):
        """Consume stderr from the Go process to prevent pipe buffer deadlocks."""
        try:
            for line in self.process.stderr:
                text = line.decode('utf-8', errors='replace').strip()
                if text:
                    print(f"[Ghost Tunnel] {text}", flush=True)
        except Exception:
            pass

    def stop(self):
        """Terminate the Ghost Tunnel process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None
            self.local_port = 0
            print("[Ghost Tunnel] Stopped.", flush=True)

    def is_running(self):
        """Check if the tunnel process is still alive."""
        if self.process is None:
            return False
        return self.process.poll() is None


def start_ghost_tunnel(profile_os, upstream_type='direct',
                       upstream_addr='', upstream_user='', upstream_pass=''):
    """
    Convenience function to start a Ghost Tunnel instance.
    Returns (tunnel_instance, local_port).
    """
    tunnel = GhostTunnel(
        profile_os=profile_os,
        upstream_type=upstream_type,
        upstream_addr=upstream_addr,
        upstream_user=upstream_user,
        upstream_pass=upstream_pass
    )
    port = tunnel.start()
    return tunnel, port
