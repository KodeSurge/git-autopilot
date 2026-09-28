"""
Unit tests for docker-compose.yml files.

Verifies that:
1. Both esp32 and esp8266 docker-compose.yml contain a 'docling' service
   with the correct image and port mapping.
2. The existing 'autopilot' service remains unchanged.
3. Both files are valid YAML with version 3.8.
"""

import os
import unittest
import yaml

# Resolve paths relative to the repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESP32_COMPOSE = os.path.join(REPO_ROOT, "esp32", "docker-compose.yml")
ESP8266_COMPOSE = os.path.join(REPO_ROOT, "esp8266", "docker-compose.yml")

EXPECTED_DCLING_IMAGE = "ghcr.io/docling-project/docling-rs-serve:latest"
EXPECTED_DCLING_PORTS = ["5001:5001"]


def load_compose(path):
    """Load and return parsed YAML data from a docker-compose file."""
    with open(path) as f:
        return yaml.safe_load(f)


class TestDoclingService(unittest.TestCase):
    """Verify the docling service is correctly defined in both compose files."""

    def test_esp32_docling_image(self):
        data = load_compose(ESP32_COMPOSE)
        docling = data["services"]["docling"]
        self.assertEqual(docling["image"], EXPECTED_DCLING_IMAGE)

    def test_esp32_docling_ports(self):
        data = load_compose(ESP32_COMPOSE)
        docling = data["services"]["docling"]
        self.assertEqual(docling["ports"], EXPECTED_DCLING_PORTS)

    def test_esp8266_docling_image(self):
        data = load_compose(ESP8266_COMPOSE)
        docling = data["services"]["docling"]
        self.assertEqual(docling["image"], EXPECTED_DCLING_IMAGE)

    def test_esp8266_docling_ports(self):
        data = load_compose(ESP8266_COMPOSE)
        docling = data["services"]["docling"]
        self.assertEqual(docling["ports"], EXPECTED_DCLING_PORTS)

    def test_esp32_services_contain_autopilot_and_docling(self):
        data = load_compose(ESP32_COMPOSE)
        self.assertIn("autopilot", data["services"])
        self.assertIn("docling", data["services"])

    def test_esp8266_services_contain_autopilot_and_docling(self):
        data = load_compose(ESP8266_COMPOSE)
        self.assertIn("autopilot", data["services"])
        self.assertIn("docling", data["services"])


class TestAutopilotServiceUnchanged(unittest.TestCase):
    """Verify the existing autopilot service definitions are unchanged."""

    def test_esp32_autopilot_image(self):
        data = load_compose(ESP32_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertEqual(autopilot["image"], "kodesurge/autopilot-esp32:latest")

    def test_esp32_autopilot_ports(self):
        data = load_compose(ESP32_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertEqual(autopilot["ports"], ["8081:8081"])

    def test_esp32_autopilot_privileged(self):
        data = load_compose(ESP32_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertTrue(autopilot["privileged"])

    def test_esp8266_autopilot_image(self):
        data = load_compose(ESP8266_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertEqual(autopilot["image"], "kodesurge/autopilot-esp8266:latest")

    def test_esp8266_autopilot_ports(self):
        data = load_compose(ESP8266_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertEqual(autopilot["ports"], ["8081:8081"])

    def test_esp8266_autopilot_privileged(self):
        data = load_compose(ESP8266_COMPOSE)
        autopilot = data["services"]["autopilot"]
        self.assertTrue(autopilot["privileged"])


class TestYAMLStructure(unittest.TestCase):
    """Verify YAML structure and version."""

    def test_esp32_version(self):
        data = load_compose(ESP32_COMPOSE)
        self.assertEqual(data["version"], "3.8")

    def test_esp8266_version(self):
        data = load_compose(ESP8266_COMPOSE)
        self.assertEqual(data["version"], "3.8")


if __name__ == "__main__":
    unittest.main()
