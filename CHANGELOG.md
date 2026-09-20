# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-09-20
### Added
- Standardized release version 2.0.0 across all components.
- Version-aware User-Agent parsing in `stealth_engine.py` (Chromium 151+).
- Added `offline_enabled` to extension manifest.

### Fixed
- Fixed critical `WebRTCProxy` reassignment bug in `inject.js` which caused failures in strict mode.
- Fixed duplicate imports and variable declarations in `server.py` for cleaner code and slightly lower overhead.
- Fixed `is_port_open` duplicate function definitions in `server.py`.
- Fixed `matrix_bg.js` idle sleep logic to correctly stop `requestAnimationFrame` and conserve GPU/CPU power.
- Fixed error handlers returning HTML/plain text for `/api` endpoints by correctly forcing `Content-Type: application/json`.

### Removed
- Removed unused `cdp_injector.py` and `ghostcore_extension/rabbit.js`.
- Removed `profiles.json` and `proxies.json` test data files from version control to prevent exposing proxy IPs and credentials.
