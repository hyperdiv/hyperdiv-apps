import datetime
import hyperdiv as hd
from .notes_db import (
    create_empty_note,
    read_note,
    get_notes,
    save_note,
    delete_note,
)

router = hd.router()


def extract_title(note_body):
    if not note_body:
        return ""
    else:
        return note_body.split("\n", 1)[0].lstrip(" #")


def format_timestamp(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    time = dt.strftime("%-I:%M%p").lower()
    day = dt.strftime("%b %d")
    return f"{day} {time}"


@hd.global_state
class NotesTask(hd.task):
    def run(self):
        super().run(get_notes)


@router.route("/note/{note_id}")
def edit_note(note_id):
    # Task that loads the note from the DB
    edited_note_task = hd.task()
    edited_note_task.run(read_note, note_id)

    # If the note hasn't loaded yet, we render nothing.
    if not edited_note_task.done:
        return

    window = hd.window()
    notes_task = NotesTask()
    state = hd.state(editing=False)

    note = edited_note_task.result

    if note is None:
        hd.text("This note does not exist.")
        return

    # If the note is empty, open the editor by default.
    if not note["note_body"]:
        state.editing = True

    if not state.editing:
        with hd.hbox(gap=0.5):
            if hd.button("Edit", prefix_icon="pencil", size="small").clicked:
                state.editing = True
        hd.markdown(note["note_body"])
        return

    note_editor = hd.textarea(
        height="100%",
        input_base_style=hd.style(height="100%"),
        input_wrapper_style=hd.style(height="100%"),
        input_style=hd.style(height="100%", font_family="mono"),
        placeholder="Type your note here, using Markdown.",
        value=note["note_body"],
        collect=False,
    )

    with hd.hbox(gap=0.5):
        save_button = hd.button(
            "Save",
            prefix_icon="download",
            size="small",
            disabled=not note_editor.value and not note["note_body"],
        )
        cancel_button = hd.button(
            "Cancel",
            prefix_icon="x",
            size="small",
            disabled=not note_editor.value and not note["note_body"],
        )

    if window.width < 1200:
        # On small screens, render the editor and preview in tabs.
        with hd.box(height="100%", gap=0.5):
            tabs = hd.tabs("Edit", "Preview")
            if tabs.active == "Edit":
                note_editor.collect()
            else:
                hd.markdown(note_editor.value)
    else:
        # On large screens, render them side by side.
        with hd.hbox(gap=1, vertical_scroll=False, height="100%"):
            with hd.box(width="50%", height="100%"):
                note_editor.collect()
            with hd.box(width="50%", vertical_scroll=True):
                hd.markdown(note_editor.value)

    if save_button.clicked:
        save_note(
            note_id,
            extract_title(note_editor.value),
            note_editor.value,
        )
        # Clear the task so the note re-renders with the
        # new content.
        edited_note_task.clear()
        # Clear the notes task, so the list in the sidebar re-renders
        notes_task.clear()

    if save_button.clicked or cancel_button.clicked:
        note_editor.reset()
        state.editing = False


def notes_list(drawer):
    loc = hd.location()

    notes_task = NotesTask()

    # The delete confirmation dialog.
    # This state stores the note to delete:
    delete_state = hd.state(note=None)
    delete_dialog = hd.dialog("Are you sure?")
    # If the note to delete is set, populate the dialog contents:
    if delete_state.note:
        with delete_dialog:
            with hd.box(gap=2):
                note_title = delete_state.note["note_title"] or "[ New Note ]"
                hd.text(f'Are you sure you want to delete the note "{note_title}"?')
                with hd.hbox(justify="end", gap=0.5):
                    # When canceling, do nothing.
                    if hd.button("Cancel").clicked:
                        delete_dialog.opened = False
                    # If delete was clicked, delete the note and clear
                    # the notes_task, which will re-read the notes
                    # and cause the notes list to re-render:
                    if hd.button("Delete", variant="danger").clicked:
                        delete_note(delete_state.note["note_id"])
                        notes_task.clear()
                        delete_dialog.opened = False
                        if loc.path == f"/note/{delete_state.note['note_id']}":
                            loc.path = "/"

    # Render the main note list.
    if hd.button("New Note", prefix_icon="pencil", width=None, size="small").clicked:
        note_id = create_empty_note()
        notes_task.clear()
        drawer.opened = False
        loc.go(f"/note/{note_id}")

    notes_task.run()

    # We don't check for `task.done`, to avoid re-rendering
    # the whole list when the task is cleared. Instead, we
    # render the "old list" while the task is re-running.
    if notes_task.result:
        for note in notes_task.result:
            link_path = f"/note/{note['note_id']}"
            with hd.scope(note["note_id"]):
                with hd.link(
                    href=link_path,
                    background_color="neutral-100" if loc.path == link_path else None,
                    hover_background_color="neutral-50",
                    border_radius="large",
                    padding=1,
                ) as link:
                    with hd.hbox(gap=1, justify="space-between", align="center"):
                        hd.text(note["note_title"] or "[ New Note ]")
                        if hd.icon_button(
                            "x",
                            font_color="neutral-400",
                            font_size=1.5,
                            padding=0,
                        ).clicked:
                            # If delete is clicked, set the
                            # note to delete and open the
                            # dialog.
                            delete_state.note = note
                            delete_dialog.opened = True

                    hd.text(
                        format_timestamp(note["ts"]),
                        font_size="x-small",
                        font_color="neutral-400",
                    )
                if link.clicked:
                    drawer.opened = False


@router.route("/")
def home():
    hd.text("Use the sidebar to select a note or create a new one.")


@router.not_found
def not_found():
    hd.markdown(f"Invalid path: `{hd.location().path}`")


def main():
    template = hd.template(title="Note Taking App")
    template.sidebar.padding = (2, 1, 2, 1)
    with template.sidebar:
        notes_list(template.drawer)
    with template.body:
        router.run()
