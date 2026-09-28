import time
import stealth_engine

# Determine base Chromium version
try:
    major_v, full_v = stealth_engine.get_installed_chromium_version()
except Exception:
    major_v = "153"
    full_v = "153.0.0.0"

print(f"[*] Detected Chromium Base Version: {major_v}")

# Define 3 completely distinct profiles
profiles = [
    {
        "id": f"prof-win-{int(time.time())}",
        "name": "GhostCore Ultimate - Windows 11",
        "useragent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_v}.0.0.0 Safari/537.36",
        "hardware": {
            "cpuCores": 16,
            "memoryGb": 32,
            "webGlVendor": "Google Inc. (NVIDIA)",
            "webGlRenderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0)",
        }
    },
    {
        "id": f"prof-mac-{int(time.time())}",
        "name": "GhostCore Ultimate - macOS Sonoma",
        "useragent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_v}.0.0.0 Safari/537.36",
        "hardware": {
            "cpuCores": 8,
            "memoryGb": 16,
            "webGlVendor": "Google Inc. (Apple)",
            "webGlRenderer": "ANGLE (Apple, Apple M3 Max, OpenGL 4.1)",
        }
    },
    {
        "id": f"prof-lin-{int(time.time())}",
        "name": "GhostCore Ultimate - Ubuntu Linux",
        "useragent": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_v}.0.0.0 Safari/537.36",
        "hardware": {
            "cpuCores": 12,
            "memoryGb": 32,
            "webGlVendor": "Google Inc. (Intel)",
            "webGlRenderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics (CML GT2), OpenGL 4.6)",
        }
    }
]

# The major fingerprinting sites
urls = [
    "https://www.browserscan.net",
    "https://abrahamjuliot.github.io/creepjs/",
    "https://browserleaks.com/canvas"
]

print("\n" + "=" * 60)
print("  👻  GhostCore Studio - Ultimate Weapon Test Launch  👻  ")
print("=" * 60)

for p in profiles:
    print(f"\n[+] Injecting and Launching: {p['name']}")
    print(f"    - Spoofed GPU: {p['hardware']['webGlRenderer']}")
    print(f"    - Spoofed OS: {p['useragent']}")
    
    try:
        stealth_engine.launch_stealth_profile(
            profile_id=p["id"],
            name=p["name"],
            width=1920,
            height=1080,
            useragent=p["useragent"],
            proxy_str="",
            port=0,
            url=urls,
            webgl_vendor=p["hardware"]["webGlVendor"],
            webgl_renderer=p["hardware"]["webGlRenderer"],
            cpu_cores=p["hardware"]["cpuCores"],
            memory_gb=p["hardware"]["memoryGb"],
            proxy_user="",
            proxy_pass="",
            timezone_id="Asia/Kolkata",
            custom_extensions=[],
            fingerprint_seed=p["id"]
        )
        print("    --> Success! Browser process spawned.")
    except Exception as e:
        print(f"    --> Error spawning profile: {e}")
    
    # Wait a few seconds between launching profiles so they don't fight for resources simultaneously
    time.sleep(3)

print("\n[+] All 3 platforms (Windows, Mac, Linux) launched.")
print("[+] Wait for them to load the tabs and verify the spoofed data.")
