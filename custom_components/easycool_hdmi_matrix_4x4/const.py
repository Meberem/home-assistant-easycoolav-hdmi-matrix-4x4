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
EDID_OPTIONS = (
    ("EDIDD1", "1080P 2CH"),
    ("EDIDD2", "1080P 6CH"),
    ("EDIDD3", "1080P 8CH"),
    ("EDIDD4", "1080P 3D 2CH"),
    ("EDIDD5", "1080P 3D 6CH"),
    ("EDIDD6", "1080P 3D 8CH"),
    ("EDIDD7", "4K30HZ 3D 2CH"),
    ("EDIDD8", "4K30HZ 3D 6CH"),
    ("EDIDD9", "4K30HZ 3D 8CH"),
    ("EDIDD10", "4K60HZ(Y420) 3D 2CH"),
    ("EDIDD11", "4K60HZ(Y420) 3D 6CH"),
    ("EDIDD12", "4K60HZ(Y420) 3D 8CH"),
    ("EDIDD13", "4K60HZ 3D 2CH"),
    ("EDIDD14", "4K60HZ 3D 6CH"),
    ("EDIDD15", "4K60HZ 3D 8CH"),
    ("EDIDD16", "1080P 2CH HDR"),
    ("EDIDD17", "1080P 6CH HDR"),
    ("EDIDD18", "1080P 8CH HDR"),
    ("EDIDD19", "1080P 3D 2CH HDR"),
    ("EDIDD20", "1080P 3D 6CH HDR"),
    ("EDIDD21", "1080P 3D 8CH HDR"),
    ("EDIDD22", "4K30HZ 3D 2CH HDR"),
    ("EDIDD23", "4K30HZ 3D 6CH HDR"),
    ("EDIDD24", "4K30HZ 3D 8CH HDR"),
    ("EDIDD25", "4K60HZ(Y420) 3D 2CH HDR"),
    ("EDIDD26", "4K60HZ(Y420) 3D 6CH HDR"),
    ("EDIDD27", "4K60HZ(Y420) 3D 8CH HDR"),
    ("EDIDD28", "4K60HZ 3D 2CH HDR"),
    ("EDIDD29", "4K60HZ 3D 6CH HDR"),
    ("EDIDD30", "4K60HZ 3D 8CH HDR"),
    ("EDIDU1", "User1 EDID"),
    ("EDIDU2", "User2 EDID"),
    ("EDIDU3", "User3 EDID"),
    ("EDIDO1", "Copy From HDMI Out1"),
    ("EDIDO2", "Copy From HDMI Out2"),
    ("EDIDO3", "Copy From HDMI Out3"),
    ("EDIDO4", "Copy From HDMI Out4"),
    ("EDIDTO1", "Copy From HDBT Out1"),
    ("EDIDTO2", "Copy From HDBT Out2"),
    ("EDIDTO3", "Copy From HDBT Out3"),
    ("EDIDTO4", "Copy From HDBT Out4"),
)


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


def merge_entry_data(data: dict[str, object], options: dict[str, object]) -> dict[str, object]:
    """Return config entry data with options taking precedence."""
    return {**data, **options}
