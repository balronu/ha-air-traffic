"""Shared test configuration; HA fixtures are supplied in CI only."""

pytest_plugins = ("pytest_homeassistant_custom_component",)

try:
    import pytest_homeassistant_custom_component  # noqa: F401
except ImportError:  # pragma: no cover - local offline environment
    pass
