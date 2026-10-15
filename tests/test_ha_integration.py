"""Home Assistant runtime tests, executed in the pinned CI environment."""

from __future__ import annotations

try:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry
except ImportError:  # pragma: no cover - expected on the local offline runner
    HomeAssistant = None
else:
    from const import (
        CONF_ADSB_ENTITY,
        CONF_ADSB_SOURCE,
        CONF_ENABLE_TRACKING,
        CONF_SCAN_INTERVAL,
        CONF_SOURCE_MODE,
        DOMAIN,
    )

    def _adsb_data() -> dict:
        return {
            CONF_SOURCE_MODE: "adsb_only",
            CONF_ADSB_SOURCE: "entity",
            CONF_ADSB_ENTITY: "sensor.adsb_feed",
            CONF_SCAN_INTERVAL: 10,
            CONF_ENABLE_TRACKING: False,
        }

    def _set_adsb_state(hass: HomeAssistant) -> None:
        hass.states.async_set(
            "sensor.adsb_feed",
            "1",
            {
                "aircraft": [
                    {
                        "hex": "abc123",
                        "flight": " TEST123 ",
                        "lat": 50.0,
                        "lon": 8.0,
                        "alt_baro": 12000,
                        "gs": 410,
                        "track": 90,
                    }
                ],
                "messages": 7,
                "now": 1700000000,
            },
        )

    async def test_config_flow_supports_adsb_entity_and_normalizes_url(
        hass: HomeAssistant, enable_custom_integrations
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SOURCE_MODE: "adsb_only", CONF_ENABLE_TRACKING: False},
        )
        assert result["step_id"] == "adsb_source"
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ADSB_SOURCE: "entity", CONF_SCAN_INTERVAL: 10},
        )
        assert result["step_id"] == "adsb_entity"
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ADSB_ENTITY: "sensor.adsb_feed"}
        )
        assert result["type"] == "create_entry"
        assert result["data"][CONF_ADSB_ENTITY] == "sensor.adsb_feed"

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "user"}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SOURCE_MODE: "adsb_only", CONF_ENABLE_TRACKING: False},
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ADSB_SOURCE: "url", CONF_SCAN_INTERVAL: 10},
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"adsb_url": "http://adsb.local:8080"}
        )
        assert result["type"] == "create_entry"
        assert result["data"]["adsb_url"].endswith("/data/aircraft.json")

    async def test_options_flow_preserves_entry_and_updates_tracking(
        hass: HomeAssistant, enable_custom_integrations
    ):
        entry = MockConfigEntry(domain=DOMAIN, data=_adsb_data())
        entry.add_to_hass(hass)

        result = await hass.config_entries.options.async_init(entry.entry_id)
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {CONF_SCAN_INTERVAL: 20, CONF_ENABLE_TRACKING: True},
        )
        assert result["type"] == "form"
        assert result["step_id"] == "tracking"
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"track_mode": "callsign", "track_callsigns": "TEST123"},
        )
        assert result["type"] == "create_entry"
        assert result["data"][CONF_SCAN_INTERVAL] == 20
        assert result["data"]["track_callsigns"] == "TEST123"

    async def test_setup_entities_coordinator_frontend_and_unload(
        hass: HomeAssistant, enable_custom_integrations
    ):
        _set_adsb_state(hass)
        entry = MockConfigEntry(domain=DOMAIN, data=_adsb_data())
        entry.add_to_hass(hass)

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        coordinator = hass.data[DOMAIN][entry.entry_id]
        assert coordinator.data.merged_count == 0
        assert coordinator.data.adsb_count == 1
        assert coordinator.data.flights[0]["callsign"] == "TEST123"
        assert coordinator.data.aircraft[0]["hex"] == "abc123"
        assert hass.data[DOMAIN]["frontend_registered"] is True

        states = [
            state
            for state in hass.states.async_all()
            if state.attributes.get("integration") == DOMAIN
        ]
        assert not states  # entities do not need an integration attribute
        assert hass.states.get(f"sensor.air_traffic_merged") is not None
        assert hass.states.get(f"sensor.air_traffic_tracked_count") is not None
        assert hass.states.get(f"binary_sensor.air_traffic_tracked_present") is not None

        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.entry_id not in hass.data[DOMAIN]
