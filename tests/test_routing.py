import unittest

from custom_components.easycool_hdmi_matrix_4x4.bridge import (
    build_button_id,
    build_route_url,
    parse_video_states,
)
from custom_components.easycool_hdmi_matrix_4x4.const import get_labels


class RoutingTests(unittest.TestCase):
    def test_build_button_id(self) -> None:
        self.assertEqual(build_button_id(1, 2), "O1I2")
        self.assertEqual(build_button_id(4, 1), "O4I1")

    def test_build_route_url(self) -> None:
        url = build_route_url(
            host="192.168.1.239",
            port=80,
            ssl=False,
            path="/",
            output=2,
            input_num=3,
            nonce=12345,
        )
        self.assertEqual(
            url,
            "http://192.168.1.239:80/TimSendCmd.CGI?button=O2I3+12345",
        )

    def test_parse_video_states(self) -> None:
        states = parse_video_states("VidSta=O1I3&O2I1&O3I1&O4I1")
        self.assertEqual(states, {1: 3, 2: 1, 3: 1, 4: 1})

    def test_configured_labels(self) -> None:
        labels = get_labels(
            {
                "input_label_1": "Apple TV",
                "input_label_2": "Chromecast",
                "input_label_3": "PC",
                "input_label_4": "Console",
            },
            "input_labels",
            "input_label_{}",
            ["Input 1", "Input 2", "Input 3", "Input 4"],
        )
        self.assertEqual(labels[0], "Apple TV")


if __name__ == "__main__":
    unittest.main()
