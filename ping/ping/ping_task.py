import hyperdiv as hd
import time
import subprocess
from .state import PingState


def ping(hostname):
    p = subprocess.Popen(["ping", "-c", "1", hostname], stdout=subprocess.PIPE)
    out, err = p.communicate()
    return float(out.split(b"\n")[1].split(b" ")[-2].split(b"=")[1])


def ping_task():
    state = PingState()
    state.stop_event.clear()

    while True:
        now = int(time.time() * 1000)

        # Get a copy of the ping values
        ping_values = state.get_ping_values()

        # Update the copy
        for host in ping_values:
            try:
                ping_value = ping(host)
            except Exception as e:
                hd.logger.warn(f"Ping Failed for {host}: {e}")
                ping_value = None
            ping_values[host] = ping_values[host][-20:] + ((now, ping_value),)

        # Update the master with the copy
        state.update_ping_values(ping_values)

        if state.stop_event.wait(1):
            break
