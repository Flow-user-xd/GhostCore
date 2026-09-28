import codecs
data = codecs.open('src/data/deviceCatalog.js', 'r', 'utf-8').read()
data = data.replace('Chrome/153.0.0.0', 'Chrome/" + (window.detectedMajorVersion || "153") + ".0.0.0')
codecs.open('src/data/deviceCatalog.js', 'w', 'utf-8').write(data)
