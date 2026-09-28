// GhostCore Profile Config - Base Template
(function() {
  const cfg = {
    profileId: 'default-profile',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    chromeMajorVersion: '153',
    chromeFullVersion: '153.0.8010.36',
    canvasR: 0,
    canvasG: 0,
    canvasB: 0,
    canvasStride: 8,
    webglVendor: 'Google Inc. (NVIDIA)',
    webglRenderer: 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)',
    cpuCores: 8,
    memoryGb: 8,
    audioNoise: 0.00000005
  };
  if (typeof self !== 'undefined' && typeof window === 'undefined') {
    self.__GHOST_CONFIG = cfg;
    self.__OMNI_CONFIG = cfg;
  }
  if (typeof window !== 'undefined') {
    try {
      Object.defineProperty(window, '__ghost_tmp_cfg__', {
        value: cfg,
        configurable: true,
        enumerable: false,
        writable: true
      });
      Object.defineProperty(window, '__omni_tmp_cfg__', {
        value: cfg,
        configurable: true,
        enumerable: false,
        writable: true
      });
    } catch (e) {
      window.__GHOST_CONFIG = cfg;
      window.__OMNI_CONFIG = cfg;
    }
  }
})();
