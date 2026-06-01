# CYD Dashboard — cyd-3dprinter-HA-integration

> A feature-rich ESPHome dashboard for the **Cheap Yellow Display (CYD)** that monitors your Bambu Lab 3D printer in real time through Home Assistant.

![Banner](docs/images/banner.png)

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
| ![Orbit](docs/images/theme-orbit.png) | ![Tactical](docs/images/theme-tactical.png) | ![Blueprint](docs/images/theme-blueprint.png) |

| Monitor | Brutal | Apple |
|---------|--------|-------|
| ![Monitor](docs/images/theme-monitor.png) | ![Brutal](docs/images/theme-brutal.png) | ![Apple](docs/images/theme-apple.png) |

| Modern Grid | Skeuomorphic |
|-------------|--------------|
| ![Grid](docs/images/theme-grid.png) | ![Skeuo](docs/images/theme-skeuo.png) |

> 📁 Replace the placeholder images in `docs/images/` with your own screenshots.

---

## ⚡ Quick Start — no clone required

You can use this dashboard **without cloning the repository**. ESPHome will download the dashboard automatically from GitHub.

### 1 — Create your device config

Copy [`YOUR-PRINTER.yaml.example`](YOUR-PRINTER.yaml.example), rename it (e.g. `my-x1c.yaml`) and fill in your printer entities:

```yaml
substitutions:
  device_name: my-cyd-dashboard
  friendly_name: My 3D Print Dashboard
  short_name: X1C

  printer_progress_entity: sensor.YOUR_PRINTER_print_progress
  printer_nozzle_entity:   sensor.YOUR_PRINTER_nozzle_temperature
  printer_bed_entity:      sensor.YOUR_PRINTER_bed_temperature
  printer_time_entity:     sensor.YOUR_PRINTER_remaining_time
  printer_layer_entity:    sensor.YOUR_PRINTER_current_layer
  printer_total_layer_entity: sensor.YOUR_PRINTER_total_layers
  printer_state_entity:    sensor.YOUR_PRINTER_print_stage
  printer_start_time_entity: sensor.YOUR_PRINTER_start_time
  printer_end_time_entity:   sensor.YOUR_PRINTER_end_time
  printer_power_entity:    sensor.YOUR_PRINTER_power
  quick_action_entity:     switch.YOUR_PRINTER
  ha_clock_entity:         sensor.time

packages:
  dashboard:
    url: https://github.com/maelr/cyd-bambu-dashboard
    file: packages/cyd-dashboard.yaml
    ref: main
    refresh: 1d
```

### 2 — Create your `secrets.yaml`

```yaml
wifi_ssid: "YourNetwork"
wifi_password: "YourPassword"
ha_api_key: "your-esphome-api-key"   # esphome generate-secrets
ota_password: "your-ota-password"
wifi_ap_password: "your-ap-password"
```

### 3 — Flash

```bash
esphome run my-x1c.yaml
```

That's it. No local files beyond your config and secrets needed. ESPHome fetches the dashboard code and all defaults from GitHub, caches it locally, and refreshes once per day.

> **Tip:** To pin to a specific version instead of always tracking `main`, replace `ref: main` with a tag or commit SHA, e.g. `ref: v1.0.0`.

---

## 🛒 Hardware

| Component | Details |
|-----------|---------|
| **ESP32 board** | CYD (Cheap Yellow Display) — ESP32 + ILI9341 + XPT2046 |
| **Display** | ILI9341 320×240 px TFT, SPI |
| **Touch** | XPT2046 resistive touchscreen |
| **RGB LED** | Built-in on CYD |

> Any CYD variant with the standard pinout will work. The default pins are configured for the most common version.

---

## 🧰 Prerequisites

- [ESPHome](https://esphome.io) ≥ 2025.2.0 (CLI or Home Assistant add-on)
- [Home Assistant](https://www.home-assistant.io) with the **Bambu Lab integration** installed
- A **Bambu Lab X1C** (or adapt the entity IDs for other models — see [Configuration](#configuration))

---

## 🚀 Installation

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cyd-bambu-dashboard.git
cd cyd-bambu-dashboard
```

### 2 — Create your `secrets.yaml`

Copy the example and fill in your own values:

```bash
cp secrets.yaml.example secrets.yaml
```

Edit `secrets.yaml`:

```yaml
wifi_ssid: "YourNetworkName"
wifi_password: "YourWiFiPassword"
ha_api_key: "your-esphome-api-encryption-key"   # generate with: esphome generate-secrets
ota_password: "your-ota-password"
wifi_ap_password: "fallback-ap-password"
```

> ⚠️ `secrets.yaml` is excluded from Git by `.gitignore`. Never commit it.

### 3 — Configure your printer entities

Open `packages/cyd-x1c-substitutions.yaml` and update the entity IDs to match your Bambu Lab integration:

```yaml
printer_progress_entity: sensor.YOUR_PRINTER_print_progress
printer_nozzle_entity:   sensor.YOUR_PRINTER_nozzle_temperature
printer_bed_entity:      sensor.YOUR_PRINTER_bed_temperature
printer_time_entity:     sensor.YOUR_PRINTER_remaining_time
printer_layer_entity:    sensor.YOUR_PRINTER_current_layer
printer_total_layer_entity: sensor.YOUR_PRINTER_total_layers
printer_state_entity:    sensor.YOUR_PRINTER_print_stage
printer_start_time_entity: sensor.YOUR_PRINTER_start_time
printer_end_time_entity:   sensor.YOUR_PRINTER_end_time
printer_power_entity:    sensor.YOUR_PRINTER_power
quick_action_entity:     switch.YOUR_PRINTER   # optional power switch
```

You can find your entity IDs in Home Assistant under **Settings → Devices & Services → Bambu Lab**.

### 4 — Flash the device

```bash
# First flash (USB)
esphome run cyd-x1c.yaml

# Subsequent updates (OTA)
esphome run cyd-x1c.yaml
```

---

## ⚙️ Configuration

### Project structure

```
esphome/
├── cyd-x1c.yaml                      # Main config (packages + esphome stack)
├── packages/
│   └── cyd-x1c-substitutions.yaml    # All substitutions for the X1C
├── secrets.yaml                       # Your credentials — NOT committed
├── secrets.yaml.example               # Template to share safely
└── .gitignore
```

### Adapting for another printer model

1. Duplicate `packages/cyd-x1c-substitutions.yaml` → e.g. `packages/cyd-p1s-substitutions.yaml`
2. Update `device_name`, `friendly_name`, `short_name` and all `printer_*_entity` values
3. Duplicate `cyd-x1c.yaml` → `cyd-p1s.yaml` and change the include:
   ```yaml
   packages:
     substitutions: !include packages/cyd-p1s-substitutions.yaml
   ```
4. Flash with `esphome run cyd-p1s.yaml`

### Touch calibration

If touches are inaccurate, adjust in `packages/cyd-x1c-substitutions.yaml`:

```yaml
touch_cal_x_min: "280"
touch_cal_x_max: "3860"
touch_cal_y_min: "340"
touch_cal_y_max: "3860"
```

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

**Swipe right-to-left** → next theme  
**Swipe left-to-right** → next palette

Both are exposed as `select` entities in Home Assistant (`CYD X1C Dashboard Theme` / `Palette`) and persist across reboots.

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

## 🔧 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Touch is off / inverted | Adjust `touch_cal_*` and `touch_swap_xy` / `touch_mirror_*` substitutions |
| Display is mirrored | Set `display_mirror_x` or `display_mirror_y` to `"true"` |
| No printer data | Check entity IDs in `cyd-x1c-substitutions.yaml` match your HA integration |
| Theme not restored after reboot | ESPHome saves theme index to NVS — first reboot after flash resets to default |
| WiFi fallback AP active | Connect to `CYD-X1C-Fallback` with `wifi_ap_password` from `secrets.yaml` |

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
