from __future__ import annotations

import random
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


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
