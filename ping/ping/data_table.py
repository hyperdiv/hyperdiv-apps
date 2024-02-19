import hyperdiv as hd
from .state import PingState


def row_delete_button(hostname):
    """
    The delete button for each table row. If only one row exists, the
    delete button is disabled.
    """
    state = PingState()

    with hd.box(padding=1):
        if hd.icon_button(
            "x", font_color="red", disabled=len(state.ping_values) <= 1
        ).clicked:
            state.remove_host(hostname)


def get_minmax_value(fn, pings):
    if not pings:
        return "?"
    if any(t is None for _, t in pings):
        return "?"
    return fn(t for _, t in pings)


def get_minmax_columns(ping_values):
    return (
        [get_minmax_value(min, v) for v in ping_values],
        [get_minmax_value(max, v) for v in ping_values],
    )


def data_table():
    state = PingState()

    host_column = tuple(state.ping_values.keys())
    min_column, max_column = get_minmax_columns(state.ping_values.values())

    hd.data_table(
        {
            "Hostname": host_column,
            "Min": min_column,
            "Max": max_column,
        },
        row_actions=row_delete_button,
        id_column_name="Hostname",
    )
