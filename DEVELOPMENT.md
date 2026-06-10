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
