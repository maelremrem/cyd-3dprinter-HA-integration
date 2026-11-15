# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Switched the default ILI9341 CYD display from `mipi_spi` to `ili9xxx` to work around screen corruption/streaking (#8, #9) and the invalid-offsets config error (#6) on ESPHome 2026.6+.
- Documented CYD display revision limits, regression checks, and the upstream `ili9xxx` deprecation (removal planned for ESPHome 2027.5.0).

- Removed seconds from theme clocks so the header time displays as `HH:MM`.
- Left-anchored the Tactical, Orbit, and Monitor header clocks to reduce visual jitter when the time changes.
- Widened Orbit and Monitor header clocks so two-digit hours (e.g. `20:05`) are not clipped.
- Split temperature units into smaller labels so `C` renders at a reduced size next to the numeric value.
- Improved quick panel footer spacing so the IP address no longer pushes the online status off-screen.
- Normalized quick panel switch and power status casing from `on`/`off` to `On`/`Off`.
- Replaced deprecated ESPHome IP address string formatting to stay compatible with ESPHome 2026.8.0 and newer.
