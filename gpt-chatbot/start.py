import sys
import os
import openai
import hyperdiv as hd

key_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "key.txt",
)

try:
    with open(key_path) as f:
        openai.api_key = f.read().strip()
except Exception as e:
    print(f"Could not read OpenAI API key: {e}")
    sys.exit(1)


def add_message(role, content, state, gpt_model):
    state.messages += (
        dict(role=role, content=content, id=state.message_id, gpt_model=gpt_model),
    )
    state.message_id += 1


def request(gpt_model, state):
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[dict(role=m["role"], content=m["content"]) for m in state.messages],
        temperature=0,
        stream=True,
    )

    for chunk in response:
        message = chunk["choices"][0]["delta"]
        state.current_reply += message.get("content", "")

    add_message("assistant", state.current_reply, state, gpt_model)
    state.current_reply = ""


def render_user_message(content, gpt_model):
    with hd.hbox(
        align="center",
        padding=0.5,
        border_radius="medium",
        background_color="neutral-50",
        font_color="neutral-600",
        justify="space-between",
    ):
        with hd.hbox(gap=0.5, align="center"):
            hd.icon("chevron-right", shrink=0)
            hd.text(content)
        hd.badge(gpt_model)


def main():
    state = hd.state(messages=(), current_reply="", gpt_model="gpt-4", message_id=0)

    task = hd.task()

    template = hd.template(title="GPT Chatbot", sidebar=False)

    with template.body:
        # Render the messages so far, if any.
        if len(state.messages) > 0:
            # We use a vertical-reverse box to render the messages, so
            # they naturally stay 'stuck' to the bottom and auto-scroll up.
            with hd.box(direction="vertical-reverse", gap=1.5, vertical_scroll=True):
                # The current reply is the most recent message
                if state.current_reply:
                    hd.markdown(state.current_reply)

                # Render the rest of the messages in reverse. The
                # `vertical-reverse` direction will re-reverse them,
                # rendering them in expected order.
                for e in reversed(state.messages):
                    with hd.scope(e["id"]):
                        if e["role"] == "system":
                            continue
                        if e["role"] == "user":
                            render_user_message(e["content"], e["gpt_model"])
                        else:
                            hd.markdown(e["content"])

        with hd.box(align="center", gap=1.5):
            # Render the input form.
            with hd.form(direction="horizontal", width="100%") as form:
                with hd.box(grow=1):
                    prompt = form.text_input(
                        placeholder="Talk to the AI",
                        autofocus=True,
                        disabled=task.running,
                        name="prompt",
                    )

                model = form.select(
                    options=("gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"),
                    value="gpt-4",
                    name="gpt-model",
                )

            if form.submitted:
                add_message("user", prompt.value, state, model.value)
                prompt.reset()
                task.rerun(request, model.value, state)

            # Render a small button that when clicked, resets the message history.
            if len(state.messages) > 0:
                if hd.button(
                    "Start Over", size="small", variant="text", disabled=task.running
                ).clicked:
                    state.messages = ()


hd.run(main)
