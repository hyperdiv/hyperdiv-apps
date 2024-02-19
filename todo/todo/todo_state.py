import hyperdiv as hd


@hd.global_state
class TodoState(hd.BaseState):
    """
    The global todos state. It exposes properties and methods for
    reading and writing that state.
    """

    # Todos are held in a prop that is a list of (string, bool)
    # tuples, where the string is the todo text and the bool
    # represents whether the todo is completed/done.
    todos = hd.Prop(
        hd.List(hd.Tuple(hd.PureString, hd.Bool)),
        (
            ("Buy groceries", True),
            ("Bike - install new tires", False),
            ("Work out", True),
        ),
    )

    def toggle_todo(self, todo):
        self.todos = tuple(
            (t, (done if t != todo else not done)) for t, done in self.todos
        )

    def remove_todo(self, todo):
        self.todos = tuple((t, done) for t, done in self.todos if t != todo)

    @property
    def items_left(self):
        return len([(t, done) for t, done in self.todos if not done])

    def clear_completed(self):
        self.todos = tuple((t, done) for t, done in self.todos if not done)

    @property
    def has_completed(self):
        return len([(t, done) for t, done in self.todos if done]) > 0

    def add_todo(self, todo):
        if todo not in (todo for todo, _ in self.todos):
            self.todos = ((todo, False),) + self.todos

    @property
    def completed_todos(self):
        return tuple((todo, done) for todo, done in self.todos if done)

    @property
    def active_todos(self):
        return tuple((todo, done) for todo, done in self.todos if not done)

    def toggle_completed_all(self):
        value = not all(done for _, done in self.todos)
        self.todos = tuple((todo, value) for todo, _ in self.todos)

    def update(self, todo, edited_todo):
        self.todos = tuple(
            (edited_todo if t == todo else t, done) for t, done in self.todos
        )
