import re

def fix_popup():
    with open('ghostcore_extension/popup.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Hardware line has weird bytes: 's Hardware' or similar
    content = re.sub(r'<span class="label">.*?Canvas Noise</span>', '<span class="label">🎨 Canvas Noise</span>', content)
    content = re.sub(r'<span class="label">.*?WebGL GPU</span>', '<span class="label">🖥️ WebGL GPU</span>', content)
    content = re.sub(r'<span class="label">.*?Hardware</span>', '<span class="label">💻 Hardware</span>', content)
    content = re.sub(r'<span class="label">.*?Timezone / Lang</span>', '<span class="label">🌍 Timezone / Lang</span>', content)
    content = re.sub(r'<span class="label">.*?WebRTC Leak</span>', '<span class="label">🌐 WebRTC Leak</span>', content)
    content = re.sub(r'<span class="label">.*?External Exts</span>', '<span class="label">🧩 External Exts</span>', content)

    with open('ghostcore_extension/popup.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed popup.html")

def fix_app_js():
    with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # We will use simple heuristics.
    # Replace single `?` or `??` based on context
    
    # Checkmarks
    content = content.replace(' Successfully', '✅ Successfully')
    content = content.replace(' Applied proxy choice', '✅ Applied proxy choice')
    content = content.replace(' Parsed & Auto-Filled', '✅ Parsed & Auto-Filled')
    content = content.replace(' Copied to Clipboard', '✅ Copied to Clipboard')
    content = content.replace(' Connection Successful', '✅ Connection Successful')
    content = content.replace(' Replaced profile database', '✅ Replaced profile database')
    content = content.replace(' Backup successfully generated', '✅ Backup successfully generated')
    content = content.replace(' Loaded ', '✅ Loaded ')
    content = content.replace(' Pasted ', '✅ Pasted ')
    content = content.replace(' Active Local Paths & Extension Sync Verified', '✅ Active Local Paths & Extension Sync Verified')
    
    # Error / Warn
    content = content.replace('? Error', '❌ Error')
    content = content.replace('? Invalid format', '❌ Invalid format')
    content = content.replace('? No valid proxies', '❌ No valid proxies')
    content = content.replace('? Please enter both Proxy', '⚠️ Please enter both Proxy')
    content = content.replace('?? Please paste a proxy', '⚠️ Please paste a proxy')
    content = content.replace('?? Failed', '❌ Failed')
    content = content.replace('? Installation failed', '❌ Installation failed')

    # Loading
    content = content.replace('? Generating...', '⏳ Generating...')
    content = content.replace('? Probing & Testing...', '⏳ Probing & Testing...')
    content = content.replace('? Testing...', '⏳ Testing...')
    content = content.replace('? Connecting & testing proxy speed...', '⏳ Connecting & testing proxy speed...')
    content = content.replace('? Initializing...', '⏳ Initializing...')
    content = content.replace('?? Downloading Chromium Portable...', '📥 Downloading Chromium Portable...')
    content = content.replace('?? Extracting Packages...', '📦 Extracting Packages...')
    content = content.replace('? Generate Profiles', '⚡ Generate Profiles')

    # Buttons
    content = content.replace('?? Copy to Clipboard', '📋 Copy to Clipboard')
    content = content.replace('?? Paste from Clipboard', '📋 Paste from Clipboard')
    content = content.replace('?? Download .bat Launcher', '💾 Download .bat Launcher')
    content = content.replace('?? Clone Profile (Specs Only)', '👯 Clone Profile (Specs Only)')
    content = content.replace('?? Clone Profile', '👯 Clone Profile')
    content = content.replace('?? Inject & Save Cookies', '🍪 Inject & Save Cookies')
    content = content.replace('?? Export Cookies (JSON)', '💾 Export Cookies (JSON)')
    content = content.replace('??? Clear All Cookies', '🗑️ Clear All Cookies')
    content = content.replace('? Clear', '🗑️ Clear')
    content = content.replace('?? Install Selected Version', '📥 Install Selected Version')
    content = content.replace('? Test All & Auto-Detect', '⚡ Test All & Auto-Detect')
    content = content.replace('?? Randomize Fingerprint', '🎲 Randomize Fingerprint')
    
    # Badges / Icons
    content = content.replace('?? Canvas 2D & WebAudio Noise: <strong>Per-Profile Unique</strong>', '🛡️ Canvas 2D & WebAudio Noise: <strong>Per-Profile Unique</strong>')
    
    content = content.replace('?? Tested', '🔍 Tested')
    content = content.replace('?? Automatically detected', '🤖 Automatically detected')
    content = content.replace('?? Freshly regenerated Canvas', '✨ Freshly regenerated Canvas')
    content = content.replace('?? Cloned specs as a new profile', '👯 Cloned specs as a new profile')
    content = content.replace('?? Cleaned up and removed', '🧹 Cleaned up and removed')
    content = content.replace('?? Successfully cloned specs', '👯 Successfully cloned specs')
    
    # Specific options
    content = content.replace('?? All 50 Desktop & Laptop Devices (Mixed)', '🖥️ All 50 Desktop & Laptop Devices (Mixed)')
    content = content.replace('?? Laptops & Ultrabooks (Dell, ThinkPad, HP, Asus)', '💻 Laptops & Ultrabooks (Dell, ThinkPad, HP, Asus)')
    content = content.replace('?? High-End Gaming & Workstations (RTX 4090/4080, Alienware)', '🎮 High-End Gaming & Workstations (RTX 4090/4080, Alienware)')
    content = content.replace('?? Apple Silicon Macs (MacBook Pro M3, Mac Studio)', '🍎 Apple Silicon Macs (MacBook Pro M3, Mac Studio)')
    content = content.replace('?? Linux Workstations (Ubuntu, Fedora)', '🐧 Linux Workstations (Ubuntu, Fedora)')
    
    content = content.replace('?? Every generated profile receives a unique Canvas seed', '💡 Every generated profile receives a unique Canvas seed')
    
    # Close buttons (which were \u00d7 × but got corrupted to ?)
    content = content.replace('>?</button>', '>×</button>')
    
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed app.js")

if __name__ == '__main__':
    fix_popup()
    fix_app_js()
