#!/usr/bin/env python3
"""
GhostCore Browser - Fingerprint Testing Suite
================================================
Launches GhostCore's calibrated stealth browser core (portable Chromium 153)
with active anti-detect protections and opens major browser fingerprinting
and bot-detection testing sites in separate tabs.

Supported Sites:
  1. BrowserScan      - https://www.browserscan.net
  2. CreepJS          - https://abrahamjuliot.github.io/creepjs/
  4. Pixelscan        - https://pixelscan.net
  5. Sannysoft Bot    - https://bot.sannysoft.com/
  6. BrowserLeaks     - https://browserleaks.com/webgl
  7. Canvas Leaks     - https://browserleaks.com/canvas
  8. WebRTC Leak      - https://browserleaks.com/ip
  9. Cover Your Tracks- https://coveryourtracks.eff.org/
 10. DeviceInfo       - https://www.deviceinfo.me/

Usage:
  python test_fingerprint.py              # Interactive selector
  python test_fingerprint.py --all        # Open all major testing sites
  python test_fingerprint.py --site browserscan # Open a specific testing site
  python test_fingerprint.py --profile 1  # Select profile by index or ID
  python test_fingerprint.py --fresh      # Use a fresh temporary profile
"""

import os
import sys
import json
import argparse
import time

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure current working directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import stealth_engine

FINGERPRINT_SITES = {
    "1": {
        "id": "browserscan",
        "name": "BrowserScan",
        "url": "https://www.browserscan.net",
        "desc": "Kernel authenticity, version detection, bot scoring & proxy/DNS leaks"
    },

    "3": {
        "id": "creepjs",
        "name": "CreepJS",
        "url": "https://abrahamjuliot.github.io/creepjs/",
        "desc": "Deep JavaScript prototype tampering, toString disguise & worker leaks"
    },
    "4": {
        "id": "pixelscan",
        "name": "Pixelscan",
        "url": "https://pixelscan.net",
        "desc": "Browser fingerprint consistency, hardware heuristics & bot detection"
    },
    "5": {
        "id": "sannysoft",
        "name": "Sannysoft Bot Test",
        "url": "https://bot.sannysoft.com/",
        "desc": "CDP automation flags, navigator.webdriver & Chrome runtime integrity"
    },
    "6": {
        "id": "webgl",
        "name": "BrowserLeaks (WebGL)",
        "url": "https://browserleaks.com/webgl",
        "desc": "WebGL unmasked vendor/renderer strings, shader precision & extensions"
    },
    "7": {
        "id": "canvas",
        "name": "BrowserLeaks (Canvas)",
        "url": "https://browserleaks.com/canvas",
        "desc": "Canvas 2D rendering entropy, noise delta & CRC32 signature verification"
    },
    "8": {
        "id": "webrtc",
        "name": "BrowserLeaks (IP / WebRTC)",
        "url": "https://browserleaks.com/ip",
        "desc": "STUN/TURN candidate leaks, local/public IP isolation & DNS inspection"
    },
    "9": {
        "id": "coveryourtracks",
        "name": "EFF Cover Your Tracks",
        "url": "https://coveryourtracks.eff.org/",
        "desc": "Tracker blocking, canvas fingerprinting & overall browser uniqueness"
    },
    "10": {
        "id": "deviceinfo",
        "name": "DeviceInfo",
        "url": "https://www.deviceinfo.me/",
        "desc": "Comprehensive inspection of hardware, screen, audio & navigator APIs"
    }
}


def load_profiles():
    """Load profiles from profiles.json if available."""
    profiles_path = os.path.join(BASE_DIR, 'profiles.json')
    if os.path.exists(profiles_path):
        try:
            with open(profiles_path, 'r', encoding='utf-8') as f:
                profs = json.load(f)
                if isinstance(profs, list) and len(profs) > 0:
                    return profs
        except Exception as e:
            print(f"[!] Warning reading profiles.json: {e}")
    return []


def create_default_test_profile():
    """Generate an authentic calibrated profile matching the installed Chromium core."""
    major_v, full_v = stealth_engine.get_installed_chromium_version()
    return {
        "id": f"prof-test-{int(time.time())}",
        "name": "GhostCore Stealth Test Suite Profile",
        "os": "Windows 11",
        "browser": f"Chrome {major_v}",
        "useragent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_v}.0.0.0 Safari/537.36",
        "resolution": {"width": 1920, "height": 1080, "dpr": 1},
        "hardware": {
            "cpuCores": 16,
            "memoryGb": 32,
            "webGlVendor": "Google Inc. (NVIDIA)",
            "webGlRenderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
            "canvasNoise": "Noise"
        },
        "proxy": {
            "enabled": False,
            "type": "SOCKS5",
            "ip": "",
            "port": "",
            "username": "",
            "password": "",
            "location": "Direct Network",
            "timezone": "Asia/Kolkata"
        }
    }


def print_banner():
    print("=" * 72)
    print("   [+]   GHOSTCORE BROWSER - FINGERPRINT TESTING SUITE   [+]")
    print("=" * 72)
    major_v, full_v = stealth_engine.get_installed_chromium_version()
    print(f"[*] Chromium Engine Core : {stealth_engine.CHROME_EXEC}")
    print(f"[*] Calibrated Version   : Chrome {major_v} ({full_v})")
    print(f"[*] Active Protections   : Canvas & Audio Noise, WebGL / WebGPU Spoofing,")
    print(f"                           MediaDevices WeakMap Disguise, Client Hints Alignment")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="GhostCore Browser Fingerprint Test Suite")
    parser.add_argument("--all", action="store_true", help="Open all major fingerprint testing sites in tabs")
    parser.add_argument("--site", type=str, help="Specific site to test (e.g. browserscan, creepjs, pixelscan, sannysoft)")
    parser.add_argument("--profile", type=str, help="Profile ID or 1-based index from profiles.json to use")
    parser.add_argument("--fresh", action="store_true", help="Always generate a fresh temporary test profile")
    parser.add_argument("--proxy", type=str, help="Custom proxy URL (e.g. socks5://ip:port or http://ip:port)")
    parser.add_argument("--port", type=int, default=9222, help="Remote debugging CDP port (default 9222)")
    args = parser.parse_args()

    print_banner()

    # 1. Select Profile
    profiles = load_profiles()
    selected_prof = None

    if args.fresh or not profiles:
        selected_prof = create_default_test_profile()
        print("\n[+] Created fresh calibrated test profile:")
    elif args.profile:
        # Check by 1-based index or ID or name
        if args.profile.isdigit() and 1 <= int(args.profile) <= len(profiles):
            selected_prof = profiles[int(args.profile) - 1]
        else:
            for p in profiles:
                if p.get("id") == args.profile or args.profile.lower() in p.get("name", "").lower():
                    selected_prof = p
                    break
        if not selected_prof:
            print(f"[!] Profile '{args.profile}' not found in profiles.json. Falling back to first available.")
            selected_prof = profiles[0]
        print(f"\n[+] Using profile from profiles.json: {selected_prof.get('name')}")
    else:
        # Interactive profile selection if multiple available
        if len(profiles) == 1:
            selected_prof = profiles[0]
            print(f"\n[+] Using loaded profile: {selected_prof.get('name')}")
        else:
            print("\nAvailable Profiles in profiles.json:")
            for i, p in enumerate(profiles):
                print(f"  [{i + 1}] {p.get('name')} ({p.get('browser', 'Chrome')})")
            print(f"  [{len(profiles) + 1}] Create a Fresh Calibrated Profile")
            choice = input(f"\nSelect a profile [1-{len(profiles) + 1}] (Default: 1): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(profiles):
                selected_prof = profiles[int(choice) - 1]
            elif choice == str(len(profiles) + 1):
                selected_prof = create_default_test_profile()
            else:
                selected_prof = profiles[0]
            print(f"[+] Selected profile: {selected_prof.get('name')}")

    # 2. Select Sites to Test
    target_urls = []
    if args.all:
        target_urls = [s["url"] for s in FINGERPRINT_SITES.values()]
    elif args.site:
        target_site = args.site.lower()
        matched = None
        for s in FINGERPRINT_SITES.values():
            if s["id"] == target_site or target_site in s["name"].lower():
                matched = s["url"]
                break
        if matched:
            target_urls = [matched]
        else:
            print(f"[!] Unknown site '{args.site}'. Opening all sites instead.")
            target_urls = [s["url"] for s in FINGERPRINT_SITES.values()]
    else:
        # Interactive Site Selection
        print("\nSelect Fingerprint Testing Sites:")
        print("  [0]  [*] ALL Major Sites (Opens each in a separate tab - Recommended)")
        for key, info in FINGERPRINT_SITES.items():
            print(f"  [{key.rjust(2)}] {info['name'].ljust(26)} - {info['desc']}")

        site_choice = input("\nEnter site choice [0-10] (Default: 0 for ALL): ").strip()
        if site_choice == "0" or not site_choice:
            target_urls = [s["url"] for s in FINGERPRINT_SITES.values()]
            print("[+] Opening all 10 major testing sites simultaneously in separate tabs.")
        elif site_choice in FINGERPRINT_SITES:
            chosen = FINGERPRINT_SITES[site_choice]
            target_urls = [chosen["url"]]
            print(f"[+] Opening {chosen['name']} ({chosen['url']}).")
        else:
            print("[!] Invalid choice. Defaulting to all sites.")
            target_urls = [s["url"] for s in FINGERPRINT_SITES.values()]

    # Extract specs from profile
    prof_id = selected_prof.get("id", f"prof-{int(time.time())}")
    prof_name = selected_prof.get("name", "Stealth Test Profile")
    res = selected_prof.get("resolution", {})
    width = res.get("width", 1920)
    height = res.get("height", 1080)
    ua = selected_prof.get("useragent", "")
    hw = selected_prof.get("hardware", {})
    cpu_cores = hw.get("cpuCores", 16)
    memory_gb = hw.get("memoryGb", 32)
    webgl_vendor = hw.get("webGlVendor", "Google Inc. (NVIDIA)")
    webgl_renderer = hw.get("webGlRenderer", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)")
    proxy_info = selected_prof.get("proxy", {})
    tz = proxy_info.get("timezone", "Asia/Kolkata")

    proxy_str = ""
    proxy_user = ""
    proxy_pass = ""
    if args.proxy:
        proxy_str = args.proxy
    elif proxy_info.get("enabled") and proxy_info.get("ip") and proxy_info.get("port"):
        ptype = proxy_info.get("type", "SOCKS5").lower()
        ip = proxy_info.get("ip")
        port = proxy_info.get("port")
        proxy_str = f"{ptype}://{ip}:{port}"
        proxy_user = proxy_info.get("username", "")
        proxy_pass = proxy_info.get("password", "")

    print("\n" + "-" * 72)
    print("Launching Stealth Browser Instance:")
    print(f"  • Profile ID   : {prof_id}")
    print(f"  • Profile Name : {prof_name}")
    print(f"  • Resolution   : {width}x{height}")
    print(f"  • GPU / Vendor : {webgl_vendor} / {webgl_renderer}")
    print(f"  • Hardware     : {cpu_cores} Cores, {memory_gb}GB RAM")
    print(f"  • Timezone     : {tz}")
    print(f"  • Proxy        : {proxy_str if proxy_str else 'Direct Network'}")
    print(f"  • Tabs to open : {len(target_urls)}")
    for u in target_urls:
        print(f"    - {u}")
    print("-" * 72)
    print("[*] Spawning browser... Please wait while CDP & extension calibrate.\n")

    # Launch browser through stealth engine with multiple URLs
    try:
        proc = stealth_engine.launch_stealth_profile(
            profile_id=prof_id,
            name=prof_name,
            width=width,
            height=height,
            useragent=ua,
            proxy_str=proxy_str,
            port=args.port,
            url=target_urls,
            webgl_vendor=webgl_vendor,
            webgl_renderer=webgl_renderer,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            proxy_user=proxy_user,
            proxy_pass=proxy_pass,
            timezone_id=tz,
            webrtc="Proxy IP"
        )
        print("[+] Browser successfully launched!")
        print("[+] Inspect the open tabs to observe the fingerprint authenticity scores.")
        print("\n(Press Ctrl+C in this terminal when finished to close or disconnect)")
        
        # Keep process alive while browser is open
        while proc and proc.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Exiting test runner.")
    except Exception as e:
        print(f"\n[!] Error launching browser: {e}")


if __name__ == "__main__":
    main()
