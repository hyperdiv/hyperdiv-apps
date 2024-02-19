import hyperdiv as hd
from .todo_state import TodoState


def header():
    """
    The header containing the "complete all" button and input form.
    """
    todos = TodoState()

    with hd.hbox(
        padding=1,
        gap=1,
        align="center",
        border_bottom="1px solid neutral-200",
    ):
        # "Complete all" button
        with hd.box(width=3, align="center"):
            if hd.icon_button("chevron-down").clicked:
                todos.toggle_completed_all()

        # Input form
        with hd.form(direction="horizontal", grow=1) as form:
            with hd.box(grow=1):
                ti = form.text_input(
                    name="new-todo",
                    placeholder="What needs to be done?",
                )
            if ti.value:
                form.submit_button("Add", variant="success")
        if form.submitted:
            new_todo = form.form_data["new-todo"]
            if new_todo:
                todos.add_todo(new_todo)
                form.reset()


def todo_row(todo, done, last_item=False):
    """
    Renders a todo row. The check/unckeck button, the todo name, and
    delete button.
    """
    todos = TodoState()

    with hd.hbox(
        padding=1,
        gap=1,
        align="center",
        border_bottom=(None if last_item else "1px solid neutral-200"),
    ):
        # The todo toggle button
        with hd.box(width=3, align="center"):
            if done:
                kwargs = dict(
                    prefix_icon="check",
                    border="1px solid green-300",
                    font_color="green",
                    background_color="green-50",
                )
            else:
                kwargs = dict(prefix_icon="dot")

            if hd.button(border_radius="circle", **kwargs).clicked:
                todos.toggle_todo(todo)

        # The todo text. If the text is clicked, an editing form is
        # displayed. When the form is submitted, the todo is updated
        # with the new value.
        state = hd.state(editing=False)

        if not state.editing:
            if hd.link(todo, grow=1, href="", font_color="neutral-800").clicked:
                state.editing = True
            # The todo delete (x) button
            if hd.icon_button("x", font_color="red").clicked:
                todos.remove_todo(todo)

        else:
            with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box(grow=1):
                    form.text_input(value=todo, name="todo", grow=1)
                if hd.button("Cancel", variant="danger").clicked:
                    form.reset()
                    state.editing = False
                form.submit_button("Save", variant="success")

            if form.submitted:
                edited_todo = form.form_data["todo"]
                if edited_todo:
                    todos.update(todo, edited_todo)
                form.reset()
                state.editing = False


def nothing_here():
    """
    This is rendered when there are no todos to render.
    """
    with hd.box(padding=1.5, align="center", justify="center"):
        hd.text("There are no items here.", font_color="neutral-500")


def todos_list():
    """
    Renders the list of todos, conditionally based on which nav item
    is active; or the nothing_here component if there are no todos.
    """
    todos = TodoState()
    loc = hd.location()

    if loc.path == "/active":
        todo_items = todos.active_todos
    elif loc.path == "/completed":
        todo_items = todos.completed_todos
    else:
        todo_items = todos.todos

    if todo_items:
        with hd.box(vertical_scroll=True):
            for i, (todo, done) in enumerate(todo_items):
                with hd.scope(todo):
                    todo_row(todo, done, last_item=i == len(todo_items) - 1)
    else:
        nothing_here()


def link(name, path):
    """
    A nav link (All/Active/Completed) in the footer.
    """
    loc = hd.location()

    if path == loc.path:
        kwargs = dict(background_color="neutral-200")
    else:
        kwargs = dict(hover_background_color="neutral-100")

    hd.link(
        name,
        href=path,
        padding=(0.2, 0.5, 0.2, 0.5),
        font_color="neutral-800",
        font_size="small",
        border_radius="medium",
        **kwargs,
    )


def footer():
    """
    The footer, rendering the count of items left, the nav, and the
    "Clear Completed" button that is rendered conditionally only when
    there are completed items.
    """

    todos = TodoState()

    with hd.hbox(
        justify="space-between",
        align="center",
        padding=1,
        height=3,
        border_top="1px solid neutral-200",
    ):
        # Count
        hd.text(
            f"{todos.items_left} item{'s' if todos.items_left != 1 else ''} left",
            basis=0,
            grow=1,
        )

        # Nav links
        with hd.hbox(gap=1, grow=1, basis=0):
            link("All", "/")
            link("Active", "/active")
            link("Completed", "/completed")

        # Clear Completed button
        with hd.box(basis=0, grow=1, align="end"):
            if todos.has_completed:
                if hd.button("Clear Completed", size="small").clicked:
                    todos.clear_completed()


def main():
    app = hd.template(title="Todo App", sidebar=False)
    app.body.align = "center"
    with app.body:
        with hd.box(
            background_color="neutral-50",
            border="1px solid neutral-200",
            width=40,
            border_radius="large",
            vertical_scroll=False,
        ):
            header()
            todos_list()
            footer()
