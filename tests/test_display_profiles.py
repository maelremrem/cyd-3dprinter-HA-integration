"""Static checks for selectable 320x240 CYD display configurations."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT / "packages" / "cyd-dashboard-pins.yaml"
DASHBOARD = ROOT / "packages" / "cyd-dashboard.yaml"
PROFILES = ROOT / "packages" / "display-profiles"

# Controller-native dimensions before applying the landscape transform.
MIPI_NATIVE = {
    "ESP32-2432S028": (240, 320),
    "ESP32-2432S028-9342": (320, 240),
    "ESP32-2432S028-7789": (240, 320),
}
FILES = (
    "cyd-ili9341-legacy.yaml",
    "cyd-ili9341-mipi.yaml",
    "cyd-ili9342-mipi.yaml",
    "cyd-st7789v-mipi.yaml",
)


def substitutions(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)["substitutions"]


class DisplayProfilesTest(unittest.TestCase):
    def test_dashboard_exposes_common_driver_options(self):
        dashboard = DASHBOARD.read_text(encoding="utf-8")
        for name in (
            "display_driver", "display_model", "display_dimensions",
            "display_spi_mode", "display_data_rate", "display_color_order",
            "display_invert_colors", "display_swap_xy",
            "display_mirror_x", "display_mirror_y",
        ):
            self.assertIn("${" + name + "}", dashboard)
        self.assertIn("minimum_chip_revision: ${minimum_chip_revision}", dashboard)
        self.assertNotIn("sram1_as_iram: true", dashboard)

    def test_default_is_stable_and_supports_older_chips(self):
        defaults = substitutions(PINS)
        self.assertEqual(defaults["display_driver"], "ili9xxx")
        self.assertEqual(defaults["display_model"], "ILI9341")
        self.assertEqual(str(defaults["minimum_chip_revision"]), "0.0")
        self.assertEqual(defaults["display_dimensions"]["width"], 320)
        self.assertEqual(defaults["display_dimensions"]["height"], 240)

    def test_each_profile_has_valid_dimensions_and_driver_options(self):
        for filename in FILES:
            with self.subTest(profile=filename):
                profile = substitutions(PROFILES / filename)
                self.assertEqual(profile["display_spi_mode"], "MODE0")
                self.assertEqual(profile["display_dimensions"]["width"], 320)
                self.assertEqual(profile["display_dimensions"]["height"], 240)
                self.assertIn(profile["display_color_order"], ("bgr", "rgb"))
                self.assertIn(profile["display_driver"], ("ili9xxx", "mipi_spi"))

                if profile["display_driver"] == "mipi_spi":
                    model = profile["display_model"]
                    self.assertIn(model, MIPI_NATIVE)
                    width, height = MIPI_NATIVE[model]
                    if str(profile["display_swap_xy"]).lower() == "true":
                        width, height = height, width
                    dimensions = profile["display_dimensions"]
                    self.assertEqual(dimensions["width"], width)
                    self.assertEqual(dimensions["height"], height)
                    self.assertEqual(dimensions["offset_width"], 0)
                    self.assertEqual(dimensions["offset_height"], 0)
                    self.assertEqual(dimensions["pad_width"], 0)
                    self.assertEqual(dimensions["pad_height"], 0)
                else:
                    self.assertEqual(profile["display_model"], "ILI9341")
                    # The ili9xxx schema does not support mipi_spi's pad keys.
                    self.assertNotIn("pad_width", profile["display_dimensions"])
                    self.assertNotIn("pad_height", profile["display_dimensions"])


if __name__ == "__main__":
    unittest.main()
