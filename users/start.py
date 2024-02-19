import hyperdiv as hd


@hd.global_state
class UsersState(hd.BaseState):
    users = hd.Prop(
        hd.List(hd.Tuple(hd.Int, hd.PureString, hd.PureString, hd.Int)),
        (
            (0, "Olivia", "Johnson", 25),
            (1, "Liam", "Williams", 32),
            (2, "Emma", "Brown", 19),
            (3, "Noah", "Jones", 45),
            (4, "Ava", "Garcia", 28),
            (5, "Oliver", "Miller", 54),
            (6, "Sophia", "Davis", 37),
            (7, "Elijah", "Rodriguez", 22),
            (8, "Isabella", "Martinez", 30),
            (9, "William", "Hernandez", 41),
            (10, "Mia", "Lopez", 26),
            (11, "James", "Gonzalez", 35),
            (12, "Charlotte", "Wilson", 29),
            (13, "Benjamin", "Anderson", 48),
            (14, "Amelia", "Thomas", 33),
            (15, "Lucas", "Taylor", 27),
            (16, "Harper", "Moore", 24),
            (17, "Ethan", "Jackson", 39),
            (18, "Evelyn", "Martin", 31),
            (19, "Mason", "Lee", 50),
        ),
    )
    editing = hd.Prop(hd.Optional(hd.Int), None)
    deleting = hd.Prop(hd.Optional(hd.Int), None)

    def delete_user(self):
        self.users = tuple(u for u in self.users if u[0] != self.deleting)
        self.deleting = None

    def delete_users(self, user_ids):
        self.users = tuple(u for u in self.users if u[0] not in user_ids)

    def add_user(self, first_name, last_name, age):
        user_id = 0 if not self.users else max(u[0] for u in self.users) + 1
        self.users += ((user_id, first_name, last_name, age),)

    def edit_user(self, first_name, last_name, age):
        user_id = self.editing
        self.users = tuple(
            u if u[0] != user_id else (user_id, first_name, last_name, age)
            for u in self.users
        )
        self.editing = None


def confirm_delete_dialog():
    state = UsersState()

    dialog = hd.dialog("Are You Sure?")
    if state.deleting is not None:
        with dialog:
            user = next(u for u in state.users if u[0] == state.deleting)
            name = f"{user[1]} {user[2]}"
            with hd.box(gap=1):
                hd.text(f'Are you sure you want to delete "{name}"?')
                with hd.hbox(gap=1, justify="end"):
                    if hd.button("Cancel").clicked:
                        dialog.opened = False
                        state.deleting = None
                    if hd.button("Delete", variant="danger").clicked:
                        state.delete_user()
                        dialog.opened = False
    return dialog


def age_validation(age):
    try:
        if int(age) > 0:
            return
    except Exception:
        pass
    return "Invalid age."


def add_user_dialog():
    state = UsersState()

    dialog = hd.dialog("Add User")
    with dialog:
        with hd.form() as form:
            form.text_input("First Name", required=True)
            form.text_input("Last Name", required=True)
            form.text_input("Age", required=True, validation=age_validation)
            with hd.hbox(justify="end", gap=1):
                if hd.button("Cancel").clicked:
                    dialog.opened = False
                form.submit_button("Add", variant="primary")

        if form.submitted:
            first_name = form.form_data["First Name"]
            last_name = form.form_data["Last Name"]
            age = int(form.form_data["Age"])
            state.add_user(first_name, last_name, age)
            dialog.opened = False

        if dialog.was_closed:
            form.reset()

    return dialog


def edit_user_dialog():
    state = UsersState()

    dialog = hd.dialog("Edit User")
    if state.editing is not None:
        with dialog:
            user = next(u for u in state.users if u[0] == state.editing)
            user_id, first_name, last_name, age = user
            with hd.form() as form:
                form.text_input("First Name", value=first_name, required=True)
                form.text_input("Last Name", value=last_name, required=True)
                form.text_input(
                    "Age", value=age, required=True, validation=age_validation
                )
                with hd.hbox(justify="end", gap=1):
                    if hd.button("Cancel").clicked:
                        dialog.opened = False
                    form.submit_button("Save", variant="primary")

            if form.submitted:
                first_name = form.form_data["First Name"]
                last_name = form.form_data["Last Name"]
                age = int(form.form_data["Age"])
                state.edit_user(first_name, last_name, age)
                dialog.opened = False

            if dialog.was_closed:
                state.editing = None
                form.reset()

    return dialog


def users_table():
    state = UsersState()

    delete_dialog = confirm_delete_dialog()
    edit_dialog = edit_user_dialog()

    def row_actions(user_id):
        with hd.hbox(gap=0.5, padding=0.5):
            with hd.tooltip("Edit"):
                if hd.icon_button("pencil").clicked:
                    state.editing = user_id
                    edit_dialog.opened = True
            with hd.tooltip("Delete"):
                if hd.icon_button("trash").clicked:
                    state.deleting = user_id
                    delete_dialog.opened = True

    return hd.data_table(
        {
            "User ID": tuple(u[0] for u in state.users),
            "First Name": tuple(u[1] for u in state.users),
            "Last Name": tuple(u[2] for u in state.users),
            "Age": tuple(u[3] for u in state.users),
        },
        id_column_name="User ID",
        show_id_column=False,
        show_select_column=True,
        row_actions=row_actions,
        collect=False,
    )


def confirm_multi_delete_dialog(table):
    state = UsersState()
    dialog = hd.dialog("Are you sure?")
    num_users = len(table.selected_rows)
    if num_users:
        with dialog:
            hd.text(f"Delete {num_users} user{'s' if num_users != 1 else ''}?")
            with hd.hbox(gap=1, justify="end"):
                if hd.button("Cancel").clicked:
                    dialog.opened = False
                if hd.button("Delete", variant="danger").clicked:
                    state.delete_users(table.selected_rows)
                    table.reset_selected_rows()
                    dialog.opened = False
    return dialog


def table_toolbar(table):
    state = UsersState()
    add_dialog = add_user_dialog()
    delete_dialog = confirm_multi_delete_dialog(table)

    with hd.hbox(align="center", justify="space-between", gap=1):
        with hd.box():
            if table.selected_rows:
                num_users = len(table.selected_rows)
                if hd.button(
                    ("Delete User" if num_users == 1 else f"Delete {num_users} Users"),
                    prefix_icon="trash",
                    variant="danger",
                ).clicked:
                    delete_dialog.opened = True
        with hd.hbox(align="center", gap=1):
            hd.text(len(state.users), "users")
            if hd.button("Add User", prefix_icon="plus").clicked:
                add_dialog.opened = True


def main():
    app = hd.template(title="Users", sidebar=False)

    table = users_table()
    with app.body:
        table_toolbar(table)
        table.collect()


hd.run(main)
