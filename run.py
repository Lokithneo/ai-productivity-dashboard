from flask import Flask, request, redirect

app = Flask(__name__)

notes = []


@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>AI Productivity Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                text-align: center;
                padding-top: 100px;
            }
            .card {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                display: inline-block;
            }
            a {
                text-decoration: none;
                background: #00c6ff;
                padding: 10px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <h1>AI Productivity Dashboard</h1>
            <p>Smart Notes Manager</p>
            <br>
            <a href="/notes">Open Notes</a>
        </div>

    </body>
    </html>
    """


@app.route('/notes', methods=['GET', 'POST'])
def notes_page():
    global notes

    if request.method == 'POST':
        text = request.form.get('note')
        if text:
            notes.append({"text": text.strip(), "important": False})
        return redirect('/notes')

    search = request.args.get('search', '').lower()

    filtered_notes = [
        (i, n) for i, n in enumerate(notes)
        if search in n["text"].lower()
    ]

    notes_html = ""

    for i, note in filtered_notes:
        star = "⭐" if note["important"] else "☆"
        notes_html += f"""
        <div class="note {'important' if note['important'] else ''}">
            <span>{note['text']}</span>
            <div>
                <a href="/important/{i}">{star}</a>
                <a class="delete" href="/delete/{i}">✖</a>
            </div>
        </div>
        """

    return f"""
    <html>
    <head>
        <title>Notes</title>

        <style>
            body {{
                font-family: 'Segoe UI';
                margin: 0;
                transition: 0.3s;
            }}

            .light {{
                background: #f4f6f9;
                color: black;
            }}

            .dark {{
                background: #121212;
                color: white;
            }}

            .navbar {{
                padding: 15px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                background: #2a5298;
                color: white;
            }}

            .container {{
                width: 50%;
                margin: 40px auto;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                background: inherit;
            }}

            input {{
                width: 70%;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }}

            button {{
                padding: 10px;
                border: none;
                border-radius: 8px;
                background: #2a5298;
                color: white;
            }}

            .note {{
                display: flex;
                justify-content: space-between;
                padding: 10px;
                margin-top: 10px;
                border-radius: 8px;
                background: rgba(0,0,0,0.05);
            }}

            .dark .note {{
                background: rgba(255,255,255,0.1);
            }}

            .important {{
                border-left: 5px solid gold;
            }}

            .delete {{
                color: red;
                margin-left: 10px;
            }}

            .top-bar {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
            }}

            .toggle {{
                cursor: pointer;
                padding: 5px 10px;
                border-radius: 6px;
                background: #444;
                color: white;
            }}

            .clear {{
                color: red;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>

    </head>

    <body class="light" id="body">

        <div class="navbar">Notes Dashboard</div>

        <div class="container">

            <div class="top-bar">
                <form method="GET">
                    <input name="search" placeholder="Search..." value="{search}">
                </form>

                <div>
                    <span class="toggle" onclick="toggleTheme()">🌙</span>
                    <a href="/clear" class="clear">Clear All</a>
                </div>
            </div>

            <form method="POST">
                <input name="note" placeholder="Enter note..." required>
                <button>Add</button>
            </form>

            {notes_html if notes_html else "<p>No notes found</p>"}

        </div>

        <script>
            function toggleTheme() {{
                let body = document.getElementById("body");

                if (body.classList.contains("light")) {{
                    body.classList.remove("light");
                    body.classList.add("dark");
                    localStorage.setItem("theme", "dark");
                }} else {{
                    body.classList.remove("dark");
                    body.classList.add("light");
                    localStorage.setItem("theme", "light");
                }}
            }}

            // Load saved theme
            window.onload = function() {{
                let theme = localStorage.getItem("theme");
                if (theme === "dark") {{
                    document.getElementById("body").classList.remove("light");
                    document.getElementById("body").classList.add("dark");
                }}
            }}
        </script>

    </body>
    </html>
    """


@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect('/notes')


@app.route('/important/<int:index>')
def important(index):
    if 0 <= index < len(notes):
        notes[index]["important"] = not notes[index]["important"]
    return redirect('/notes')


@app.route('/clear')
def clear():
    notes.clear()
    return redirect('/notes')


if __name__ == '__main__':
    app.run(debug=True)