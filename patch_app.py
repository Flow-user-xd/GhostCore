import re
with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace single-quoted string
content = content.replace(
    "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.8010.36 Safari/537.36'",
    "`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${window.detectedFullVersion || '153.0.8010.36'} Safari/537.36`"
)

# Replace Mac string
content = content.replace(
    "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.8010.36 Safari/537.36'",
    "`Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${window.detectedFullVersion || '153.0.8010.36'} Safari/537.36`"
)

# Replace Linux string
content = content.replace(
    "'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.8010.36 Safari/537.36'",
    "`Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${window.detectedFullVersion || '153.0.8010.36'} Safari/537.36`"
)

# Fix chromePatchVersions
content = content.replace(
    "const chromePatchVersions = ['153.0.8010.36', '153.0.8010.31', '153.0.8010.25', '153.0.8010.18', '153.0.8010.12'];",
    "const chromePatchVersions = [window.detectedFullVersion || '153.0.8010.36'];"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched app.js successfully.')
