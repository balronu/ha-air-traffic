import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "custom_components" / "air_traffic_merge"))
from data import apply_tracking, merge_sources, normalize_adsb, normalize_fr24  # noqa: E402


class AirTrafficDataTests(unittest.TestCase):
    def test_adsb_normalization_preserves_missing_values(self):
        result = normalize_adsb({"flight": " DLH123 ", "hex": "abc123", "alt_baro": "not-known"})
        self.assertEqual(result["callsign"], "DLH123")
        self.assertEqual(result["hex"], "abc123")
        self.assertIsNone(result["alt_m"])
        self.assertIsNone(result["latitude"])

    def test_fr24_and_adsb_are_deduplicated_by_registration(self):
        flights = merge_sources(
            [{"aircraft_registration": "D-ABCD", "flight_number": "DLH123", "airline_short": "DLH"}],
            [{"r": "D-ABCD", "hex": "3c1234", "alt_baro": 10000, "gs": 400}],
        )
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0].source, "BOTH")
        self.assertEqual(flights[0].callsign, "DLH123")
        self.assertEqual(flights[0].airline, "DLH")
        self.assertEqual(flights[0].alt_m, 3048)

    def test_distinct_sources_remain_distinct_when_identity_differs(self):
        flights = merge_sources(
            [{"aircraft_registration": "D-ONE", "flight_number": "TEST1"}],
            [{"r": "D-TWO", "flight": "TEST2"}],
        )
        self.assertEqual({flight.source for flight in flights}, {"FR24", "ADSB"})
        self.assertEqual(len(flights), 2)

    def test_tracking_callsign_and_registration(self):
        flights = merge_sources([], [{"r": "D-ABCD", "flight": "DLH123"}, {"r": "D-EFGH", "flight": "BAW9"}])
        flights, callsigns, registrations = apply_tracking(flights, True, "both", ["DLH123"], ["D-EFGH"])
        self.assertEqual(callsigns, ["DLH123"])
        self.assertEqual(registrations, ["D-EFGH"])
        self.assertEqual(sum(flight.tracked for flight in flights), 2)

    def test_invalid_tracking_mode_falls_back_without_inventing_data(self):
        flights = merge_sources([], [{"hex": "abc", "flight": "ABC", "alt_baro": None}])
        flights, _, _ = apply_tracking(flights, True, "invalid", ["ABC"], [])
        self.assertTrue(flights[0].tracked)
        self.assertIsNone(flights[0].alt_m)


if __name__ == "__main__":
    unittest.main()
