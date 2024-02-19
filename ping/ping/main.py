import hyperdiv as hd
from .state import PingState
from .ping_task import ping_task
from .data_table import data_table


def chart():
    state = PingState()

    hd.line_chart(
        *state.ping_values.values(),
        labels=tuple(state.ping_values.keys()),
        x_axis="timeseries",
        padding=1,
        background_color="neutral-50",
        border_radius="large",
        grid_color="neutral-200",
        height=20,
        shrink=False
    )


def start_pause_button():
    lifecycle = hd.lifecycle()
    state = PingState()
    task = hd.task()

    # When the app stops, trigger the task to exit, if running.
    if lifecycle.app_stopped:
        state.stop_event.set()

    with hd.hbox(align="center", justify="center"):
        if not task.running:
            if hd.button("Start", prefix_icon="play", variant="success").clicked:
                task.rerun(ping_task)
        else:
            if hd.button("Pause", prefix_icon="pause", variant="warning").clicked:
                state.stop_event.set()


def add_host_form():
    state = PingState()

    # The form for adding a new host.
    with hd.form() as form:
        form.text_input(placeholder="Add a host", name="host")

    if form.submitted:
        host = form.form_data["host"]
        state.add_host(host)
        form.reset()


def main():
    app = hd.template(title="Ping", sidebar=False)
    app.body.padding = 4
    app.body.gap = 2
    with app.body:
        chart()
        start_pause_button()
        add_host_form()
        data_table()
