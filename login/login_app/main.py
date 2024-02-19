import hyperdiv as hd
from .users_db import get_user_by_token, check_login


def log_user_in(state, user):
    state.logged_in_user = user
    hd.local_storage.set_item("auth_token", user["token"])


def log_user_out(state):
    state.logged_in_user = None
    hd.local_storage.remove_item("auth_token")


def login_dialog(state):
    """The login screen."""

    # Look up the auth token in browser local storage.
    token_request = hd.local_storage.get_item("auth_token")

    if token_request.done:
        if token_request.result:
            user = get_user_by_token(token_request.result)
            if user:
                # If a valid token is in local storage, we
                # automatically log the user in, without showing the
                # login form.
                state.logged_in_user = user
                return

        # The login failure alert. This is `collec=False` because we
        # need to access its state in code that is lexically before
        # the spot where the alert is rendered.
        failure_alert = hd.alert(
            "Wrong user name or password",
            variant="danger",
            duration=3000,
            collect=False,
        )

        # This task is used to asynchronously check the password on
        # successful form submission.
        check_password_task = hd.task()

        # The login form container.
        with hd.box(align="center", justify="center", height="100vh", gap=1):
            if check_password_task.running:
                # If the password checking task is running, just render a
                # loading spinner.
                hd.spinner()
            else:
                # Otherwise render the login form.
                with hd.form(
                    width=30,
                    padding=2,
                    background_color="gray-50",
                    border_radius="large",
                ) as form:
                    user_name = form.text_input("User Name", required=True)
                    password = form.text_input(
                        "Password", input_type="password", required=True
                    )
                    form.submit_button("Log In", variant="primary")

                if form.submitted:
                    # This code runs when the user input the required
                    # fields and submitted the form.

                    # In case the failure alert is open from a
                    # previous failed login, close it.
                    failure_alert.opened = False
                    # Launch the password checking task.
                    check_password_task.rerun(
                        check_login,
                        user_name.value,
                        password.value,
                    )

            # Render the failure alert.
            failure_alert.collect()

        # When the password checking task completes:
        if check_password_task.finished:
            user = check_password_task.result
            if user:
                # If password checking succeeded, log the user in.
                log_user_in(state, user)
                form.reset()
            else:
                # Otherwise show the failure alert.
                failure_alert.opened = True


def main():
    state = hd.state(logged_in_user=None)

    if not state.logged_in_user:
        # If not logged in, render the login screen.
        login_dialog(state)
    else:
        # If logged in, render the main app contents.
        template = hd.template(title="My App", sidebar=False)
        with template.topbar_links:
            if hd.button("Log Out", size="small", variant="text").clicked:
                log_user_out(state)
                return
        with template.body:
            hd.h2(f"Welcome, {state.logged_in_user['name']}!")
