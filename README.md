# CYD Dashboard — cyd-3dprinter-HA-integration

> A feature-rich ESPHome dashboard for the **Cheap Yellow Display (CYD)** that monitors your 3D printer in real time through Home Assistant.

![banner](imgs/dualscreen.jpeg)

---

## ✨ Features

- 🎨 **8 themes** — Tactical, Monitor, Orbit, Blueprint, Brutal, Apple, Modern Grid, Skeuomorphic
- 🖌️ **8 color palettes** — independently selectable from themes, synced to Home Assistant
- 👆 **Swipe gestures** — left/right to cycle through themes and palettes
- 📊 **Live printer data** — progress, nozzle & bed temps, layer, time remaining, start/end time
- 🔔 **Toast notifications** — visual feedback on theme/palette changes
- 📱 **Quick panel** — overlay for settings and quick actions
- 💡 **Boot loading screen** — step-by-step startup status (WiFi, HA, UI)
- 💾 **Persistent settings** — theme and palette survive reboots
- 😴 **Auto-sleep** — backlight dims after inactivity
- 🔗 **HA sync** — theme/palette exposed as entities for automation

---

## 📸 Preview

| Orbit | Tactical | Blueprint |
|-------|----------|-----------|
| ![Orbit](imgs/orbit.jpeg) | ![Tactical](imgs/tactical.jpeg) | ![Blueprint](imgs/blueprint.jpeg) |

| Monitor | Brutal | Apple |
|---------|--------|-------|
| ![Monitor](imgs/monitor.jpeg) | ![Brutal](imgs/brutal.jpeg) | ![Apple](imgs/apple.jpeg) |

| Modern Grid | Skeuomorphic |
|-------------|--------------|
| ![Grid](imgs/grid.jpeg) | ![Skeuo](imgs/skeuomorphic.jpeg) |

> Note that some of the themes are not finished.

---

## ⚡ Quick Start — no clone required

You can use this dashboard **without cloning the repository**. ESPHome will download the dashboard automatically from GitHub.

### 1 — Create your device config

In ESPHome Builder, create a blank config, copy the example below, and fill in your printer entities:

```yaml
# ─────────────────────────────────────────────────────────────────────────────
# CYD 3D Printer Dashboard — User configuration file
# Copy this file, rename it, and fill in your own values.
#
# No clone needed — the full dashboard is loaded from GitHub automatically.
# Source: https://github.com/maelremrem/cyd-3dprinter-HA-integration
# ─────────────────────────────────────────────────────────────────────────────

substitutions:
  device_name: cyd-3d-dashboard       # ESPHome device name (no spaces)
  friendly_name: CYD 3D Dashboard     # Displayed in Home Assistant
  short_name: X1C                     # Short label shown on the display

  # ── API / OTA / Wi-Fi credentials ─────────────────────────────────────────
  # Leave these as !secret and define them in secrets.yaml.
  # Generate ha_api_key from ESPHome's API encryption key helper.
  ha_api_key: !secret ha_api_key
  ota_password: !secret ota_password
  wifi_ssid: !secret wifi_ssid
  wifi_password: !secret wifi_password

  # ── Home Assistant printer entities ────────────────────────────────────────
  # Replace each value with your own entity IDs from the Bambu Lab integration
  # (or any other printer integration exposing similar sensors)
  printer_progress_entity: sensor.YOUR_PRINTER_print_progress
  printer_nozzle_entity: sensor.YOUR_PRINTER_nozzle_temperature
  printer_bed_entity: sensor.YOUR_PRINTER_bed_temperature
  printer_time_entity: sensor.YOUR_PRINTER_remaining_time
  printer_layer_entity: sensor.YOUR_PRINTER_current_layer
  printer_total_layer_entity: sensor.YOUR_PRINTER_total_layer_count
  printer_state_entity: sensor.YOUR_PRINTER_print_status
  printer_start_time_entity: sensor.YOUR_PRINTER_start_time
  printer_end_time_entity: sensor.YOUR_PRINTER_end_time
  printer_power_entity: sensor.YOUR_PRINTER_power
  quick_action_title: "Turn on printer"
  quick_action_entity: switch.YOUR_PRINTER_switch

  ha_clock_entity: sensor.time        # Standard HA time sensor (HH:MM)


# ─────────────────────────────────────────────────────────────────────────────
# Remote package — downloads the full dashboard firmware from GitHub.
# ESPHome caches it locally and refreshes once per day.
# ─────────────────────────────────────────────────────────────────────────────
packages:
  pins: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-pins.yaml@main
  colors: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-colors.yaml@main
  dashboard: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard.yaml@main
  # Optional: add ONE profile below after 'pins' to select a different display:
  # display_profile: github://maelremrem/cyd-3dprinter-HA-integration/packages/display-profiles/cyd-st7789v-mipi.yaml@main
```

### 2 — Flash

```bash
esphome run my-x1c.yaml
```
You can also flash directly from ESPHome Builder in Home Assistant.

Using a USB cable is recommended for the first flash.

That's it. No local files beyond your config and secrets needed. ESPHome fetches the dashboard code and all defaults from GitHub, caches it locally, and refreshes once per day.

---

### 3 — Usage

There are 3 controls on the touch screen:
- **Swipe right-to-left** → next theme  
- **Swipe left-to-right** → next palette
- **Swipe down-to-up** → quick menu

You need to allow the ESPHome device to perform Home Assistant actions. See the [Home Assistant ESPHome actions guide](https://www.home-assistant.io/integrations/esphome#allow-the-device-to-perform-home-assistant-actions).

The quick menu can call `homeassistant.toggle` for `quick_action_entity`, so it works best with on/off entities such as `switch.*`.

Quick menu details:

![Quick menu](imgs/quick.jpeg)

## 🛒 Hardware

| Component | Details |
|-----------|---------|
| **ESP32 board** | CYD (Cheap Yellow Display) — ESP32 + ILI9341 + XPT2046 |
| **Display** | ILI9341 320×240 px TFT, SPI |
| **Touch** | XPT2046 resistive touchscreen |
| **RGB LED** | Built-in on CYD |

> The default configuration targets the **ILI9341-based ESP32-2432S028 / ESP32-2432S028R**, with XPT2046 resistive touch and a 320×240 landscape layout. Other compatible 320×240 CYD revisions can select a display profile as described below. Verify the actual controller and pinout; USB connector type alone is not sufficient.

---

## 🧰 Prerequisites

- [ESPHome](https://esphome.io) ≥ 2025.2.0 (CLI or Home Assistant add-on)
- [Home Assistant](https://www.home-assistant.io) with the **Bambu Lab integration** installed
- A **Bambu Lab X1C**, or another printer integration exposing similar sensors. This project was tested with [ha-bambulab](https://github.com/greghesp/ha-bambulab).

---

## 🎨 Themes & Palettes

Themes and palettes are **independent** — you can mix any theme with any palette.

| # | Theme / Palette |
|---|----------------|
| 1 | Tactical |
| 2 | Monitor |
| 3 | Orbit |
| 4 | Blueprint |
| 5 | Brutal |
| 6 | Apple |
| 7 | Modern Grid |
| 8 | Skeuomorphic |

Both are exposed as `select` entities in Home Assistant (`CYD X1C Dashboard Theme` / `Palette`) and persist across reboots.

You can create your own colors with ESPHome substitutions. If you override the palette values locally, remove or comment out the remote `colors` package.

---

## ✅ Validate Before Flashing

Before flashing, you can check that ESPHome can load the remote packages and substitutions:

```bash
esphome config my-x1c.yaml
```

Make sure your `secrets.yaml` contains `ha_api_key`, `ota_password`, `wifi_ssid`, and `wifi_password`.

---

## 🤝 Home Assistant Integration

After flashing, the device will appear automatically in Home Assistant (ESPHome integration). Exposed entities include:

| Entity | Type | Description |
|--------|------|-------------|
| `select.cyd_x1c_dashboard_theme` | Select | Current UI theme |
| `select.cyd_x1c_dashboard_palette` | Select | Current color palette |
| `sensor.cyd_x1c_dashboard_wifi_signal` | Sensor | WiFi RSSI |
| `switch.cyd_x1c_dashboard_backlight` | Switch | Display on/off |

---

## 3D Printing

I have used [this model](https://makerworld.com/en/models/2787810-cyd-desk-buddy-for-bambu-lab-home-assistant)

---

## 🖥️ CYD display/controller compatibility (ESPHome 2026.6+)

The **default remains the `ili9xxx` ILI9341 driver**, which avoids the horizontal streaking reported on some genuine CYD boards ([#9](https://github.com/maelremrem/cyd-3dprinter-HA-integration/issues/9)). Other supported controller profiles use ESPHome's newer `mipi_spi` driver.

| CYD / controller | Driver | Display profile | Status |
|---|---|---|---|
| ESP32-2432S028 / ESP32-2432S028R, ILI9341 | `ili9xxx` | `cyd-ili9341-legacy.yaml` | Default; compatibility workaround |
| Same ILI9341 boards, testing newer ESPHome driver | `mipi_spi` | `cyd-ili9341-mipi.yaml` | Experimental; #9 reports artifacts |
| 2.8" CYD, ILI9342 (some dual-USB models) | `mipi_spi` | `cyd-ili9342-mipi.yaml` | Experimental, needs device testing |
| 2.8" CYD, ST7789V (some dual-USB models) | `mipi_spi` | `cyd-st7789v-mipi.yaml` | Experimental, needs device testing |

**Choose a profile:** keep the original `pins`, `colors`, and `dashboard` packages, and append exactly one display profile after `pins`:

```yaml
packages:
  pins: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-pins.yaml@main
  colors: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-colors.yaml@main
  dashboard: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard.yaml@main
  display_profile: github://maelremrem/cyd-3dprinter-HA-integration/packages/display-profiles/cyd-st7789v-mipi.yaml@main
```

Do **not** add multiple display profiles simultaneously. With no `display_profile` package, the original ILI9341 setup remains the default. The profile sets the platform, controller model, color order, rotation/transform, and framebuffer dimensions. `mipi_spi` profiles include explicit zero offsets/padding to prevent the `Invalid offsets` error (#6).

**Manual configuration:** you can override profile substitutions in your device YAML, without editing the dashboard:

```yaml
substitutions:
  display_driver: mipi_spi
  display_model: ESP32-2432S028-7789
  display_spi_mode: MODE0
  display_data_rate: 20MHz
  display_color_order: bgr
  display_invert_colors: "false"
  display_swap_xy: "true"
  display_mirror_x: "false"
  display_mirror_y: "false"
  display_dimensions:
    width: 320
    height: 240
    offset_width: 0
    offset_height: 0
    pad_width: 0
    pad_height: 0
```

GPIOs (`pin_spi_*`, `pin_tft_*`, `pin_touch_*`, `pin_rgb_*`) and touchscreen calibration can also be overridden in device substitutions. A separate `display_dimensions` mapping is used for the panel/driver while `display_w` and `display_h` remain **logical UI dimensions**.

**Hardware limits:** these presets target **320×240 landscape** with an **XPT2046 resistive touchscreen** and the standard CYD SPI/pin mapping. Capacitive touch controllers (FT6236/GT911), 480×320 boards, circular displays, ESP32-S3 and different electrical pinouts need additional touchscreen/UI or board adaptation; selecting a display model alone is not enough.

Recompile after changing profiles (`esphome config my-x1c.yaml`, `esphome compile my-x1c.yaml`). ESPHome caches remote packages; using `@main` will only fetch the update after merge. To test a pull request, use its branch ref **on every package** rather than mixing branch and main.

**Deprecation:** ESPHome will remove `ili9xxx` in **2027.5.0**. The legacy profile is an interim compatibility fallback; validate `mipi_spi` on the affected physical board before switching permanently.

---

## 🔧 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Horizontal streaks or scrambled screen on an ILI9341 CYD | Recompile with the latest package using `ili9xxx`; verify the hardware model and try USB flashing if OTA keeps the old firmware |
| ESPHome `Invalid offsets` for `display.mipi_spi` | Recompile with the updated package, which uses `ili9xxx`. Custom `mipi_spi` configurations must provide consistent dimensions and offsets |
| Deprecated `ili9xxx` warning | Expected on ESPHome 2026.x; use a tested `mipi_spi` profile when available; removal planned for 2027.5.0 |
| Touch is off / inverted | Adjust `touch_cal_*` and `touch_swap_xy` / `touch_mirror_*` substitutions |
| Display is mirrored | Set `display_mirror_x` or `display_mirror_y` to `"true"` |
| No printer data | Check the `printer_*_entity` substitutions in your ESPHome config match your HA integration |
| Theme not restored after reboot | ESPHome saves theme index to NVS — first reboot after flash resets to default |
| Bootloop with `Required >= v3.1, found v1.1` | The updated defaults no longer require chip revision 3.1; reflash via USB if the device cannot boot |
| WiFi fallback AP active | Connect to the `CYD-<short_name>-Fallback` access point and update your Wi-Fi credentials |
