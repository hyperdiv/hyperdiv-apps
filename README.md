# Example Hyperdiv Apps

This is a collection of small Hyperdiv apps to demonstrate how such apps can be built with Hyperdiv.

* `calculator`: A simple calculator app.
* `gpt-chatbot`: A chat interface to GPT-3.5/GPT-4 using the Python wrapper to OpenAI's API.
* `image-editor`: A simple image editor that explores image parameters in realtime using sliders.
* `login`: An app showing how to implement an app protected by a login screen.
* `markdown-editor`: A simple markdown editor with live preview.
* `note-taking`: A note-taking app that uses Markdown with a live preview and stores notes in a Sqlite database. The app is responsive and renders differently depending on screen size.
* `ping`: An app that pings hostnames and plots their ping latencies on a line graph.
* `simple-todo`: A bare-bones Todo app.
* `todo`: A more full-featured Todo app.
* `users`: A users management app showing a table in action.

Click on each app directory for more info and a gif showing the running app.

## Running the Apps

After installing [Hyperdiv](https://github.com/hyperdiv/hyperdiv) and cloning this repo, install the dependencies:

```sh
pip install -r requirements.txt
```

Then run the `start.py` script in each app directory. For example:
```sh
cd gpt-chatbot
python start.py
```
