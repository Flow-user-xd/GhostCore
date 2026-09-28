import os
import sys
import zipfile
import urllib.request
import json
import shutil
import time

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CURATED_VERSIONS = [
    {
        "label": "Chromium 154 (Latest Stable - 154.0.8037.57) [Recommended]",
        "version": "154.0.8037.57",
        "tag": "154.0.8037.57-1.1",
        "major": "154",
        "url": "https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/download/154.0.8037.57-1.1/ungoogled-chromium_154.0.8037.57-1.1_windows_x64.zip"
    },
    {
        "label": "Chromium 153 (Calibrated Stable - 153.0.8010.36) [Calibrated]",
        "version": "153.0.8010.36",
        "tag": "153.0.8010.36-1.1",
        "major": "153",
        "url": "https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/download/153.0.8010.36-1.1/ungoogled-chromium_153.0.8010.36-1.1_windows_x64.zip"
    },
    {
        "label": "Chromium 151 (LTS Baseline - 151.0.7922.173)",
        "version": "151.0.7922.173",
        "tag": "151.0.7922.173-1.1",
        "major": "151",
        "url": "https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/download/151.0.7922.173-1.1/ungoogled-chromium_151.0.7922.173-1.1_windows_x64.zip"
    }
]

def get_cache_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'browser_core', 'releases_cache.json')

def fetch_all_releases(force_refresh=False):
    """
    Fetch up to 100 releases from GitHub API with local caching (12 hours).
    Returns a list of dicts: {'label', 'version', 'tag', 'major', 'url'}.
    """
    cache_path = get_cache_path()
    if not force_refresh and os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)
                if time.time() - cached.get('timestamp', 0) < 43200 and cached.get('releases'):
                    return cached['releases']
        except Exception:
            pass

    try:
        req = urllib.request.Request(
            'https://api.github.com/repos/ungoogled-software/ungoogled-chromium-windows/releases?per_page=100',
            headers={'User-Agent': 'GhostCore-Installer/2.0'}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = []
            for rel in data:
                tag = rel.get('tag_name', '')
                for asset in rel.get('assets', []):
                    name = asset.get('name', '')
                    if 'windows_x64.zip' in name and 'installer' not in name:
                        clean_ver = tag.split('-')[0]
                        major = clean_ver.split('.')[0] if '.' in clean_ver else ''
                        results.append({
                            "label": f"Chromium {clean_ver} ({tag})",
                            "version": clean_ver,
                            "tag": tag,
                            "major": major,
                            "url": asset.get('browser_download_url')
                        })
                        break
            if results:
                try:
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump({'timestamp': time.time(), 'releases': results}, f, indent=2)
                except Exception:
                    pass
                return results
    except Exception:
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                    if cached.get('releases'):
                        return cached['releases']
            except Exception:
                pass

    return CURATED_VERSIONS

def fetch_latest_releases(limit=3):
    """Return top distinct major curated or newest releases."""
    all_rels = fetch_all_releases()
    if not all_rels:
        return CURATED_VERSIONS[:limit]
    distinct = []
    seen_majors = set()
    for r in all_rels:
        m = r.get('major')
        if m and m not in seen_majors:
            seen_majors.add(m)
            distinct.append(r)
        if len(distinct) >= limit:
            break
    if len(distinct) < limit:
        distinct = all_rels[:limit]
    return distinct

def get_all_available_series():
    """Return sorted list of all available major series versions, e.g. ['154', '153', '152', ...]"""
    all_rels = fetch_all_releases()
    majors = set()
    for r in all_rels:
        m = r.get('major', '')
        if m.isdigit():
            majors.add(m)
    return sorted(list(majors), key=lambda x: int(x), reverse=True)

def fetch_series_releases(series_str):
    """Return all releases matching a specific major series (e.g. '150', '148', '149')."""
    clean_series = str(series_str).strip().lstrip('v')
    all_rels = fetch_all_releases()
    matches = []
    for r in all_rels:
        m = r.get('major', '')
        tag = r.get('tag', '')
        ver = r.get('version', '')
        if m == clean_series or ver.startswith(clean_series + '.') or tag.startswith(clean_series + '.'):
            matches.append(r)
    return matches

def probe_direct_url(tag):
    """Verify if a direct GitHub release asset URL exists via HTTP HEAD."""
    url = f"https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/download/{tag}/ungoogled-chromium_{tag}_windows_x64.zip"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GhostCore-Installer/2.0'}, method='HEAD')
        with urllib.request.urlopen(req, timeout=6) as resp:
            if resp.status in (200, 302):
                return url
    except Exception:
        pass
    return None

def fetch_specific_version(ver_input):
    """
    Search for a specific version or tag across releases, or probe direct GitHub release tags.
    Handles inputs like '150.0.7871.186', '150.0.7871.186-1.1', or '148.0.7778.215'.
    """
    if not ver_input:
        return None
    query = str(ver_input).strip().lstrip('v')
    all_rels = fetch_all_releases()

    # 1. Exact match in release list
    for r in all_rels:
        if r.get('version') == query or r.get('tag') == query:
            return r

    # 2. Prefix / partial match in release list
    for r in all_rels:
        if r.get('version', '').startswith(query) or query in r.get('tag', ''):
            return r

    # 3. Direct HEAD probe with candidate tag suffixes
    candidates = []
    if '-' in query:
        candidates.append(query)
    else:
        candidates.extend([f"{query}-1.1", f"{query}-1", f"{query}-1.2", f"{query}-2.1", query])

    for tag in candidates:
        live_url = probe_direct_url(tag)
        if live_url:
            clean_ver = tag.split('-')[0]
            major = clean_ver.split('.')[0] if '.' in clean_ver else ''
            return {
                "label": f"Chromium {clean_ver} ({tag}) [Direct Verified]",
                "version": clean_ver,
                "tag": tag,
                "major": major,
                "url": live_url
            }

    return None

def search_all_specific_versions(ver_input):
    """
    Returns a list of all matching versions for a specific string.
    Useful for frontend queries that expect multiple results.
    """
    if not ver_input:
        return []
    query = str(ver_input).strip().lstrip('v')
    all_rels = fetch_all_releases()
    
    matches = []
    
    # Prefix / partial match in release list
    for r in all_rels:
        if r.get('version', '').startswith(query) or query in r.get('tag', ''):
            matches.append(r)
            
    if matches:
        return matches

    # If no matches found in known releases, fallback to direct HEAD probe
    candidates = []
    if '-' in query:
        candidates.append(query)
    else:
        candidates.extend([f"{query}-1.1", f"{query}-1", f"{query}-1.2", f"{query}-2.1", query])

    for tag in candidates:
        live_url = probe_direct_url(tag)
        if live_url:
            clean_ver = tag.split('-')[0]
            major = clean_ver.split('.')[0] if '.' in clean_ver else ''
            matches.append({
                "label": f"Chromium {clean_ver} ({tag}) [Direct Verified]",
                "version": clean_ver,
                "tag": tag,
                "url": live_url,
                "major": major
            })
            break # Just return the first valid direct probe to save time

    return matches

def prompt_version_choice(top_versions):
    while True:
        print("\n" + "=" * 65)
        print("   [+]  GhostCore Studio -- Chromium Browser Core Setup")
        print("=" * 65)
        print("Select a portable Ungoogled Chromium version to install:\n")
        
        for i, v in enumerate(top_versions[:3], 1):
            print(f"  [{i}] {v['label']}")
        
        print("  [4] Filter by Major Series (e.g. 150, 149, 148...) -> List & Pick")
        print("  [5] Custom Specific Version (e.g. 150.0.7871.186, 148.0.7778.215)")
        print("\n" + "-" * 65)
        
        choice = input("Enter choice [1-5] (Press Enter for [1]): ").strip()
        
        if choice in ('', '1'):
            return top_versions[0]
        elif choice == '2' and len(top_versions) > 1:
            return top_versions[1]
        elif choice == '3' and len(top_versions) > 2:
            return top_versions[2]
            
        elif choice == '4':
            available_majors = get_all_available_series()
            while True:
                print("\n" + "=" * 65)
                print("   [Option 4] Filter Chromium Releases by Major Series")
                print("=" * 65)
                print(f"Available major series detected: {', '.join(available_majors[:12])}...")
                print("-" * 65)
                series_input = input("\nEnter major series (e.g. 150, 149, 148, 146) [or '0' to back]: ").strip().lower()
                
                if series_input in ('0', 'b', 'back', 'exit', 'q'):
                    break
                if not series_input:
                    continue
                    
                series_clean = series_input.lstrip('v')
                print(f"\n[*] Fetching releases for Chromium series '{series_clean}'...")
                series_releases = fetch_series_releases(series_clean)
                
                if not series_releases:
                    print(f"\n[!] No releases found for series '{series_clean}'.")
                    print(f"    Available series: {', '.join(available_majors[:12])}")
                    continue
                    
                while True:
                    print(f"\nFound {len(series_releases)} release(s) for Chromium {series_clean} series:")
                    print("-" * 65)
                    for idx, r in enumerate(series_releases, 1):
                        latest_badge = " [Latest in series]" if idx == 1 else ""
                        print(f"  [{idx}] {r['label']}{latest_badge}")
                    print("  [0] Back to series selection")
                    print("-" * 65)
                    
                    sub_choice = input(f"Select version [1-{len(series_releases)}] (Press Enter for [1], '0' for back): ").strip()
                    if sub_choice == '0':
                        break
                    if sub_choice in ('', '1'):
                        return series_releases[0]
                    try:
                        sub_idx = int(sub_choice) - 1
                        if 0 <= sub_idx < len(series_releases):
                            return series_releases[sub_idx]
                        else:
                            print(f"[!] Please enter a number between 1 and {len(series_releases)}.")
                    except ValueError:
                        print(f"[!] Invalid input. Please enter a number between 1 and {len(series_releases)}.")
                        
        elif choice == '5':
            while True:
                print("\n" + "=" * 65)
                print("   [Option 5] Install Specific Chromium Version")
                print("=" * 65)
                ver_input = input("Enter specific version or tag (e.g. 150.0.7871.186, 148.0.7778.215) [or '0' to back]: ").strip()
                
                if ver_input in ('0', 'b', 'back', 'exit', 'q'):
                    break
                if not ver_input:
                    continue
                    
                print(f"\n[*] Searching releases and verifying asset for version '{ver_input}'...")
                specific = fetch_specific_version(ver_input)
                if specific:
                    print(f"\n[+] Successfully verified release package:")
                    print(f"    Label:   {specific['label']}")
                    print(f"    Version: {specific['version']}")
                    print(f"    URL:     {specific['url']}\n")
                    confirm = input("Proceed with installation of this version? [Y/n]: ").strip().lower()
                    if confirm in ('', 'y', 'yes'):
                        return specific
                else:
                    print(f"\n[!] Could not locate a verified Windows x64 release for '{ver_input}'.")
                    print("    Examples of valid versions: 154.0.8037.57, 150.0.7871.186, 148.0.7778.215")
                    print("    Please verify the version and try again.\n")
        else:
            print("[!] Invalid selection. Please enter a number between 1 and 5.")

def download_and_setup_portable_chromium(force_interactive=False, chosen_version=None, progress_callback=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'browser_core')
    chrome_exec = os.path.join(target_dir, 'chrome.exe')

    if os.path.exists(chrome_exec) and not force_interactive and not chosen_version:
        print(f"[Portable Engine] Portable Chromium already installed at: {chrome_exec}")
        return chrome_exec

    versions = fetch_latest_releases(3)
    if chosen_version:
        if isinstance(chosen_version, dict):
            selected = chosen_version
        else:
            ver_str = str(chosen_version).strip()
            selected = fetch_specific_version(ver_str)
            if not selected and ver_str.isdigit() and len(ver_str) <= 3:
                series_rels = fetch_series_releases(ver_str)
                if series_rels:
                    selected = series_rels[0]
            if not selected:
                try:
                    idx = int(ver_str) - 1
                    if 0 <= idx < len(versions):
                        selected = versions[idx]
                except Exception:
                    pass
            if not selected:
                selected = next((v for v in versions if ver_str in v.get('version', '') or ver_str in v.get('label', '')), None)
            if not selected:
                selected = versions[0]
    elif force_interactive:
        selected = prompt_version_choice(versions)
    else:
        selected = versions[0]

    url = selected['url']

    print(f"\n[Portable Engine] Selected: {selected['label']}")
    print(f"[Portable Engine] Downloading from: {url}")
    if progress_callback:
        progress_callback({"status": "starting", "percent": 0, "label": selected['label'], "version": selected.get('version', '')})

    os.makedirs(target_dir, exist_ok=True)
    zip_path = os.path.join(base_dir, 'chromium_portable.zip')
    if os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception:
            pass

    try:
        total_size = 0
        try:
            head_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
            with urllib.request.urlopen(head_req, timeout=10) as h_resp:
                total_size = int(h_resp.headers.get('content-length', 0))
        except Exception:
            pass

        max_retries = 10
        for attempt in range(max_retries):
            downloaded = os.path.getsize(zip_path) if os.path.exists(zip_path) else 0
            if total_size > 0 and downloaded >= total_size:
                print("\n[Portable Engine] Download complete!")
                break

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            if downloaded > 0:
                headers['Range'] = f"bytes={downloaded}-"

            try:
                req = urllib.request.Request(url, headers=headers)
                mode = 'ab' if downloaded > 0 else 'wb'
                with urllib.request.urlopen(req, timeout=30) as resp, open(zip_path, mode) as out:
                    if total_size == 0 and resp.headers.get('content-length'):
                        total_size = downloaded + int(resp.headers.get('content-length'))

                    block_size = 1024 * 128
                    last_cb_time = 0
                    while True:
                        buffer = resp.read(block_size)
                        if not buffer:
                            break
                        downloaded += len(buffer)
                        out.write(buffer)
                        percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
                        mb_done = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024) if total_size > 0 else 0
                        sys.stdout.write(f"\r[Portable Engine] Downloading: {percent}% [{mb_done:.1f} MB / {mb_total:.1f} MB]")
                        sys.stdout.flush()

                        cur_time = time.time()
                        if progress_callback and (cur_time - last_cb_time > 0.5 or downloaded >= total_size):
                            last_cb_time = cur_time
                            progress_callback({
                                "status": "downloading",
                                "percent": percent,
                                "mb_done": round(mb_done, 1),
                                "mb_total": round(mb_total, 1),
                                "label": selected['label']
                            })

                if total_size > 0 and downloaded >= total_size:
                    break
            except Exception as retry_err:
                print(f"\n[Portable Engine] Download interrupted ({retry_err}). Retrying attempt {attempt + 1}/{max_retries} in 2s...")
                time.sleep(2)

        print("\n[Portable Engine] Download finished! Extracting packages...")
        if progress_callback:
            progress_callback({"status": "extracting", "percent": 100, "label": selected['label']})

        extract_tmp = os.path.join(base_dir, 'extract_tmp')
        if os.path.exists(extract_tmp):
            shutil.rmtree(extract_tmp, ignore_errors=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_tmp)

            found_dir = None
            for root, dirs, files in os.walk(extract_tmp):
                if 'chrome.exe' in files:
                    found_dir = root
                    break

            if found_dir:
                shutil.copytree(found_dir, target_dir, dirs_exist_ok=True)
                shutil.rmtree(extract_tmp, ignore_errors=True)
                print(f"[Portable Engine] Portable Chromium successfully installed to:\n  {chrome_exec}")

        if os.path.exists(zip_path):
            os.remove(zip_path)

        if progress_callback:
            progress_callback({"status": "ready", "percent": 100, "chromePath": chrome_exec})

        return chrome_exec

    except Exception as e:
        print(f"\n[Portable Engine Error] Failed to setup portable Chromium: {e}")
        if progress_callback:
            progress_callback({"status": "error", "error": str(e)})
        return None

if __name__ == '__main__':
    force = '--choose' in sys.argv or '--interactive' in sys.argv
    chosen = None
    for arg_idx, arg in enumerate(sys.argv):
        if arg in ('--choice', '-c', '--version', '-v') and arg_idx + 1 < len(sys.argv):
            chosen = sys.argv[arg_idx + 1]
            break
        elif arg in ('--series', '-s') and arg_idx + 1 < len(sys.argv):
            chosen = sys.argv[arg_idx + 1]
            break
    download_and_setup_portable_chromium(force_interactive=force, chosen_version=chosen)
