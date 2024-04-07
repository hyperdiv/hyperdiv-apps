import hyperdiv as hd
from .expr import (
    Const,
    render_output,
    render_expr,
    process_numeric_input,
    process_operator,
)


def button(label, background_color="blue", width=5, pill=False, circle=True):
    return hd.button(
        label,
        width=width,
        height=5,
        circle=circle,
        pill=pill,
        font_size=1.8,
        label_style=hd.style(align="center", justify="center"),
        background_color=background_color,
        font_color="neutral-50",
    )


def main():
    # The calculator state, initialized with the expression "0":
    state = hd.state(expr=Const("0"))

    # A container to center the calculator with padding around it:
    with hd.box(padding=4, align="center"):
        # The calculator container:
        with hd.box(
            border="1px solid gray-200",
            padding=(1, 2, 2, 2),
            gap=1,
            border_radius="x-large",
            background_color="gray-100",
            align="center",
        ):
            hd.text(
                "Hyperdiv Calculator",
                font_family="mono",
                font_color="neutral-600",
            )
            # The calculator display. We use
            # direction="horizontal-reverse" so the display is
            # naturally right-justified and sticks to the right as it
            # overflows and starts scrolling.
            with hd.box(
                background_color="gray-50",
                border="1px solid gray-300",
                border_radius="medium",
            ):
                # The main display, showing the current number or
                # result in large font:
                with hd.box(
                    direction="horizontal-reverse",
                    height=6,
                    width=24,
                    padding=1,
                    horizontal_scroll=True,
                ):
                    hd.text(
                        render_output(state.expr),
                        font_family="mono",
                        font_size=3,
                        white_space="nowrap",
                    )
                hd.divider()
                # The secondary "expression" display, showing the
                # current, partially evaluated expression, in small
                # font:
                with hd.box(
                    direction="horizontal-reverse",
                    background_color="gray-50",
                    horizontal_scroll=True,
                    border_radius="medium",
                    width=24,
                    padding=(0.1, 0.5, 0.1, 0.5),
                    font_color="neutral-500",
                ):
                    hd.text(
                        render_expr(state.expr),
                        font_family="mono",
                        white_space="nowrap",
                    )

            # The five rows of calculator buttons:
            with hd.hbox(gap=1, padding_top=1):
                if button("Clear", "gray", width=17, circle=False, pill=True).clicked:
                    state.expr = Const("0")
                if button("/", "yellow").clicked:
                    state.expr = process_operator(state.expr, "/")
            with hd.hbox(gap=1):
                if button("7").clicked:
                    state.expr = process_numeric_input(state.expr, "7")
                if button("8").clicked:
                    state.expr = process_numeric_input(state.expr, "8")
                if button("9").clicked:
                    state.expr = process_numeric_input(state.expr, "9")
                if button("*", "yellow").clicked:
                    state.expr = process_operator(state.expr, "*")
            with hd.hbox(gap=1):
                if button("4").clicked:
                    state.expr = process_numeric_input(state.expr, "4")
                if button("5").clicked:
                    state.expr = process_numeric_input(state.expr, "5")
                if button("6").clicked:
                    state.expr = process_numeric_input(state.expr, "6")
                if button("-", "yellow").clicked:
                    state.expr = process_operator(state.expr, "-")
            with hd.hbox(gap=1):
                if button("1").clicked:
                    state.expr = process_numeric_input(state.expr, "1")
                if button("2").clicked:
                    state.expr = process_numeric_input(state.expr, "2")
                if button("3").clicked:
                    state.expr = process_numeric_input(state.expr, "3")
                if button("+", "yellow").clicked:
                    state.expr = process_operator(state.expr, "+")
            with hd.hbox(gap=1):
                if button("0", width=11, pill=True, circle=False).clicked:
                    state.expr = process_numeric_input(state.expr, "0")
                if button(".").clicked:
                    state.expr = process_numeric_input(state.expr, ".")
                if button("=", "yellow").clicked:
                    state.expr = process_operator(state.expr, "=")
