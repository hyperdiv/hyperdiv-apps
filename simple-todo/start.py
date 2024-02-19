"""
A bare-bones todo app that allows adding todos, lists todos, and
when a todo is clicked, it is toggled. Completed todos are rendered as
strikethrough text.
"""

import hyperdiv as hd


class Todos:
    """
    The todos state. Note that we could inherit from hd.BaseState here
    and define a `todos` prop, but instead we choose to use a private
    state variable created with hd.state.
    """

    def __init__(self):
        self.state = hd.state(
            todos={
                "Meet Joe for lunch": False,
                "Fix bycicle": True,
                "Buy groceries": False,
            }
        )

    @property
    def todo_list(self):
        return self.state.todos.items()

    def add_todo(self, todo):
        if todo not in self.state.todos:
            # Note that the `|` operator is important because it
            # creates a new dictionary object.
            # `self.state.todos[todo] = False` would not work.
            # Also note that the `|=` operator would not work, since
            # it mutates the left-hand side value in place.
            # We could also do:
            #    new_dict = dict(**self.state.todos)
            #    new_dict[todo] = False
            #    self.state.todos = new_dict
            self.state.todos = {todo: False} | self.state.todos

    def todo_is_done(self, todo):
        return self.state.todos[todo]

    def toggle_todo(self, todo):
        self.state.todos = self.state.todos | {todo: not self.state.todos[todo]}


def main():
    todos = Todos()

    # Outer container that centers the title and inner container.
    with hd.box(gap=2, padding=4, align="center"):
        # Title
        hd.markdown("# Simple Todo App")
        # Inner container with the core functionality in it
        with hd.box(gap=2, width=40):
            # Input form
            with hd.form() as form:
                form.text_input(placeholder="Enter a todo", name="todo")
            if form.submitted:
                todo = form.form_data["todo"]
                if todo:
                    todos.add_todo(todo)
                form.reset()

            # Bullet-list of todos
            with hd.list():
                for todo, done in todos.todo_list:
                    with hd.scope(todo):
                        with hd.list_item():
                            with hd.link(
                                href="", font_color="neutral-800"
                            ) as todo_link:
                                if todos.todo_is_done(todo):
                                    hd.markdown(f"~~{todo}~~")
                                else:
                                    hd.markdown(todo)
                            if todo_link.clicked:
                                todos.toggle_todo(todo)


if __name__ == "__main__":
    hd.run(main)
