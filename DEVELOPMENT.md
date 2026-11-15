# Development

## Testing Local Package Changes

The example ESPHome configuration loads packages from GitHub:

```yaml
packages:
  pins: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-pins.yaml@main
  colors: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard-colors.yaml@main
  dashboard: github://maelremrem/cyd-3dprinter-HA-integration/packages/cyd-dashboard.yaml@main
```

When testing local changes in ESPHome Builder, copy the package files into the ESPHome config directory, for example:

```text
/config/esphome/packages/cyd-dashboard-pins.yaml
/config/esphome/packages/cyd-dashboard-colors.yaml
/config/esphome/packages/cyd-dashboard.yaml
```

Then replace the GitHub package URLs in your device config with local includes:

```yaml
packages:
  pins: !include packages/cyd-dashboard-pins.yaml
  colors: !include packages/cyd-dashboard-colors.yaml
  dashboard: !include packages/cyd-dashboard.yaml
```

After testing, switch those entries back to the GitHub package URLs, or point them at a branch while a pull request is under review.

## CYD display regression checklist

The default package uses `ili9xxx` (ILI9341) to avoid the display corruption
reported in #8 and #9 and the `mipi_spi` offsets validation error in #6.

To test this pull request before merging, point all three GitHub package URLs
in the example device configuration at `@fix/ili9xxx-display-compat` instead
of `@main`. (Do not mix package branches.) Then run:

```bash
esphome config my-x1c.yaml
esphome compile my-x1c.yaml
esphome run my-x1c.yaml
```

On a genuine ESP32-2432S028R with ILI9341 and **no PSRAM**, verify:

- No invalid-offsets validation errors or build failures.
- No horizontal streaks, corruption, or white screen from the first frame.
- UI appears in landscape; touchscreen positions and swipes are correct.
- Multiple themes and palettes render normally; progress, temperature,
  remaining time, and quick actions still work.
- Screen wake/sleep, Wi-Fi recovery, and reboot work.
- Try the ESPHome versions reported in the issues (2026.6.1, 2026.8.2)
  and a current supported version when possible.

Do not mark display issues resolved solely from static validation: hardware
confirmation is required. The `ili9xxx` driver is scheduled for removal in
ESPHome 2027.5.0, so a separate future migration to `mipi_spi` is needed.
