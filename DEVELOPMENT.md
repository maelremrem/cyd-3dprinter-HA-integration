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
of `@main`. (Do not mix package branches.) To test another controller, add
a fourth package pointing at one of `packages/display-profiles/*.yaml` on
the same branch. Then run:

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

## Profile matrix and static tests

Run the static profile regression checks:

```bash
python3 -m pip install pyyaml
python3 -m unittest discover -s tests -v
```

Compile/flash **each** profile separately (ILI9341 legacy, ILI9341 mipi,
ILI9342 mipi, ST7789V mipi) before marking it hardware verified.

Expected baseline:
- All four profiles preserve the 320x240 landscape LVGL/touch area.
- mipi_spi profiles explicitly provide 0 offsets and 0 padding.
- The default pin package remains backward-compatible without a profile.
- RGB pins use the same GPIO4/GPIO16/GPIO17 outputs as the previous code.
- Minimum ESP32 chip revision is 0.0 (fixing the reported rev 1.1 bootloop);
  the risky bootloader-dependent sram1_as_iram override is removed.
- Capacitive-touch and non-320x240 layouts are *not* yet supported by these profiles.

The static unittest does not execute ESPHome codegen or validate actual SPI
timing. Run `esphome config`, `esphome compile` and real CYD hardware tests.
