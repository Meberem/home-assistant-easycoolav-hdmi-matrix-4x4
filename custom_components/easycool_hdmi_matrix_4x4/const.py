DOMAIN = "easycool_hdmi_matrix_4x4"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_SSL = "ssl"
CONF_PATH = "path"
CONF_INPUT_LABELS = "input_labels"
CONF_OUTPUT_LABELS = "output_labels"
CONF_INPUT_LABEL_FORMAT = "input_label_{}"
CONF_OUTPUT_LABEL_FORMAT = "output_label_{}"
CONF_INPUT_LABEL_1 = "input_label_1"
CONF_INPUT_LABEL_2 = "input_label_2"
CONF_INPUT_LABEL_3 = "input_label_3"
CONF_INPUT_LABEL_4 = "input_label_4"
CONF_OUTPUT_LABEL_1 = "output_label_1"
CONF_OUTPUT_LABEL_2 = "output_label_2"
CONF_OUTPUT_LABEL_3 = "output_label_3"
CONF_OUTPUT_LABEL_4 = "output_label_4"
DEFAULT_PORT = 80
DEFAULT_SSL = False
DEFAULT_PATH = "/"
OUTPUT_COUNT = 4
INPUT_COUNT = 4
DEFAULT_INPUT_LABELS = [f"Input {index}" for index in range(1, INPUT_COUNT + 1)]
DEFAULT_OUTPUT_LABELS = [f"Output {index}" for index in range(1, OUTPUT_COUNT + 1)]


def get_labels(
    data: dict[str, object],
    list_key: str,
    item_key_format: str,
    defaults: list[str],
) -> list[str]:
    """Return configured labels from entry data or defaults."""
    labels = data.get(list_key)
    if isinstance(labels, list) and all(isinstance(item, str) for item in labels):
        if len(labels) == len(defaults):
            return labels

    parsed: list[str] = []
    for index, default in enumerate(defaults, start=1):
        key = item_key_format.format(index)
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            parsed.append(value.strip())
        else:
            parsed.append(default)
    return parsed
