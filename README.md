# Home Assistant HDMI matrix integration

This workspace contains a simple Home Assistant custom integration that maps the routing buttons from the provided web interface into Home Assistant selectors.

Product: https://www.easycoolav.com/products/4k60-444-hdmi-matrix-4x4-dolby-vision-with-audio-breakout-ip-rs232-ir-control-hdcp22-18g-bps

## What it does
- Exposes one selector per output, for outputs 1-4.
- Sends the same CGI command pattern used by the web UI: `TimSendCmd.CGI?button=O<output>I<input>+<random>`.
- Supports configuring the device host, port, SSL, and path.

## Files
- [custom_components/hdmi_matrix/bridge.py](custom_components/hdmi_matrix/bridge.py) contains the URL builder and request sender.
- [custom_components/hdmi_matrix/select.py](custom_components/hdmi_matrix/select.py) creates the Home Assistant selectors.
- [tests/test_routing.py](tests/test_routing.py) covers the button ID and URL generation.

## Verification
Run the unit tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
