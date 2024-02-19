import threading
import hyperdiv as hd


@hd.global_state
class PingState(hd.BaseState):
    # For locking access to `ping_values`, since it is accessed from
    # both the main thread + the task thread.
    lock = hd.Prop(hd.Any, None)
    # When this event is set, the task exits.
    stop_event = hd.Prop(hd.Any, None)
    # Maps hostname to a tuple of (timestamp, ping_time) values.
    ping_values = hd.Prop(hd.Any, {"github.com": ()})

    def __init__(self):
        super().__init__()
        # The first time this state is instantiated, we create the
        # lock and event.
        if self.lock is None:
            self.lock = threading.Lock()
        if self.stop_event is None:
            self.stop_event = threading.Event()

    def get_ping_values(self):
        with self.lock:
            return dict(**self.ping_values)

    def update_ping_values(self, ping_values):
        with self.lock:
            # Update values, only for existing hosts. It's possible
            # that while the ping task was updating its copy of the
            # data, hosts were deleted or added from the master copy.
            self.ping_values = {
                h: ping_values[h] if h in ping_values else self.ping_values[h]
                for h in self.ping_values
            }

    def add_host(self, host):
        with self.lock:
            if host not in self.ping_values:
                self.ping_values = self.ping_values | {host: ()}

    def remove_host(self, host):
        with self.lock:
            self.ping_values = {h: v for h, v in self.ping_values.items() if h != host}
