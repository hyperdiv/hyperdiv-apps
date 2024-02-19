import os
import sys
import hyperdiv as hd

if len(sys.argv) <= 1:
    print(f"Usage: python {sys.argv[0]} <file>")
    sys.exit(1)

if not os.path.exists(sys.argv[1]):
    contents = ""
else:
    try:
        with open(sys.argv[1]) as f:
            contents = f.read()
    except Exception as e:
        print(f"Could not open the file: {e}")
        sys.exit(1)


def save(contents):
    with open(sys.argv[1], "w") as f:
        f.write(contents)


def main():
    state = hd.state(old_contents=contents, contents=contents)

    template = hd.template(title="Markdown Editor", sidebar=False)
    template.topbar_links.gap = 1
    template.topbar_links.padding_right = 0.5

    with template.topbar_links:
        autosave = hd.switch("Autosave", size="small")
        save_button = hd.button(
            "Save",
            variant=("warning" if state.old_contents != state.contents else "success"),
            size="small",
            disabled=autosave.checked,
        )

        if save_button.clicked or (autosave.changed and autosave.checked):
            state.old_contents = state.contents
            save(state.contents)

    with template.body:
        with hd.hbox(gap=0.5, align="center"):
            hd.icon("file-text")
            hd.text(sys.argv[1], font_family="mono")

        with hd.hbox(gap=1, vertical_scroll=False, height="100%"):
            with hd.box(width="50%", height="100%"):
                ta = hd.textarea(
                    height="100%",
                    input_base_style=hd.style(height="100%"),
                    input_wrapper_style=hd.style(height="100%"),
                    input_style=hd.style(height="100%", font_family="mono"),
                    value=contents,
                )
                if ta.changed:
                    state.contents = ta.value
                    if autosave.checked:
                        state.old_contents = state.contents
                        save(state.contents)

            with hd.box(width="50%", vertical_scroll=True):
                hd.markdown(ta.value)


hd.run(main)
