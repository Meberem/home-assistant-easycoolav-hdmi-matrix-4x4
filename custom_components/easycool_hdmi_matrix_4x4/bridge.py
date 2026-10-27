from __future__ import annotations

import random
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .const import EDID_OPTIONS


def parse_video_states(payload: str) -> dict[int, int]:
    """Parse the device's VidSta response into output->input mapping."""
    if not payload:
        return {}
    if payload.startswith("VidSta="):
        payload = payload.split("=", 1)[1]
    states: dict[int, int] = {}
    for index, token in enumerate(payload.split("&"), start=1):
        if token.startswith("O") and "I" in token:
            output_num = int(token[1:token.index("I")])
            input_num = int(token[token.index("I") + 1 :])
            states[output_num] = input_num
    return states


def build_button_id(output_num: int, input_num: int) -> str:
    """Create the button identifier used by the matrix web UI."""
    if not 1 <= output_num <= 4:
        raise ValueError("output_num must be between 1 and 4")
    if not 1 <= input_num <= 4:
        raise ValueError("input_num must be between 1 and 4")
    return f"O{output_num}I{input_num}"


def build_route_url(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    output: int = 1,
    input_num: int = 1,
    nonce: int | None = None,
) -> str:
    """Build the CGI URL that the matrix web UI uses for routing."""
    scheme = "https" if ssl else "http"
    if nonce is None:
        nonce = random.randint(100000, 999999)
    button_id = build_button_id(output, input_num)
    clean_path = path or "/"
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"
    if clean_path == "/":
        path_prefix = "/"
    else:
        path_prefix = clean_path if clean_path.endswith("/") else f"{clean_path}/"
    return f"{scheme}://{host}:{port}{path_prefix}TimSendCmd.CGI?button={button_id}+{nonce}"


def send_route(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    output: int = 1,
    input_num: int = 1,
    nonce: int | None = None,
    timeout: int = 10,
) -> dict[int, int]:
    """Issue the routing command and read back the current routing state."""
    route_url = build_route_url(host, port, ssl, path, output, input_num, nonce)
    route_request = Request(route_url, method="GET")
    with urlopen(route_request, timeout=timeout) as route_response:
        route_payload = route_response.read().decode("utf-8", errors="ignore")

    state_url = build_state_url(host, port, ssl, path, nonce=nonce)
    state_request = Request(state_url, method="GET")
    with urlopen(state_request, timeout=timeout) as state_response:
        state_payload = state_response.read().decode("utf-8", errors="ignore")

    return parse_video_states(state_payload or route_payload)


def read_state(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    nonce: int | None = None,
    timeout: int = 10,
) -> dict[int, int]:
    """Read the current video state from the matrix device."""
    state_url = build_state_url(host, port, ssl, path, nonce)
    state_request = Request(state_url, method="GET")
    with urlopen(state_request, timeout=timeout) as state_response:
        state_payload = state_response.read().decode("utf-8", errors="ignore")

    return parse_video_states(state_payload)


def build_state_url(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    nonce: int | None = None,
) -> str:
    """Build the video state endpoint used by the web UI."""
    scheme = "https" if ssl else "http"
    if nonce is None:
        nonce = random.randint(100000, 999999)
    clean_path = path or "/"
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"
    if clean_path == "/":
        path_prefix = "/"
    else:
        path_prefix = clean_path if clean_path.endswith("/") else f"{clean_path}/"
    return f"{scheme}://{host}:{port}{path_prefix}VIDDivSta.CGI?{nonce}"


def parse_edid_states(payload: str) -> dict[int, str]:
    """Parse the device's EdidSta response into input->EDID token mapping."""
    if not payload:
        return {}
    if payload.startswith("EdidSta="):
        payload = payload.split("=", 1)[1]
    return {
        input_num: token
        for input_num, token in enumerate(payload.split("&"), start=1)
        if input_num <= 4 and token
    }


def build_edid_url(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    input_num: int = 1,
    edid_token: str = "EDIDD1",
    nonce: int | None = None,
) -> str:
    """Build the CGI URL used to apply an EDID to one HDMI input."""
    if not 1 <= input_num <= 4:
        raise ValueError("input_num must be between 1 and 4")
    if edid_token not in {token for token, _label in EDID_OPTIONS}:
        raise ValueError("Unknown EDID token")
    scheme = "https" if ssl else "http"
    if nonce is None:
        nonce = random.randint(100000, 999999)
    clean_path = path or "/"
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"
    if clean_path == "/":
        path_prefix = "/"
    else:
        path_prefix = clean_path if clean_path.endswith("/") else f"{clean_path}/"
    return (
        f"{scheme}://{host}:{port}{path_prefix}EdidsendCmd.CGI?"
        f"button={edid_token}IN{input_num}+{nonce}"
    )


def build_edid_state_url(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    nonce: int | None = None,
) -> str:
    """Build the EDID state endpoint used by the web UI."""
    scheme = "https" if ssl else "http"
    if nonce is None:
        nonce = random.randint(100000, 999999)
    clean_path = path or "/"
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"
    if clean_path == "/":
        path_prefix = "/"
    else:
        path_prefix = clean_path if clean_path.endswith("/") else f"{clean_path}/"
    return f"{scheme}://{host}:{port}{path_prefix}EDIDDivSta.CGI?{nonce}"


def read_edid_state(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    nonce: int | None = None,
    timeout: int = 10,
) -> dict[int, str]:
    """Read the current EDID assignment for each HDMI input."""
    state_url = build_edid_state_url(host, port, ssl, path, nonce)
    state_request = Request(state_url, method="GET")
    with urlopen(state_request, timeout=timeout) as state_response:
        state_payload = state_response.read().decode("utf-8", errors="ignore")
    return parse_edid_states(state_payload)


def send_edid(
    host: str,
    port: int = 80,
    ssl: bool = False,
    path: str = "/",
    input_num: int = 1,
    edid_token: str = "EDIDD1",
    nonce: int | None = None,
    timeout: int = 10,
) -> dict[int, str]:
    """Apply an EDID to an input and read back all current assignments."""
    command_url = build_edid_url(host, port, ssl, path, input_num, edid_token, nonce)
    command_request = Request(command_url, method="GET")
    with urlopen(command_request, timeout=timeout) as command_response:
        command_payload = command_response.read().decode("utf-8", errors="ignore")

    state_url = build_edid_state_url(host, port, ssl, path, nonce=nonce)
    state_request = Request(state_url, method="GET")
    with urlopen(state_request, timeout=timeout) as state_response:
        state_payload = state_response.read().decode("utf-8", errors="ignore")
    return parse_edid_states(state_payload or command_payload)
