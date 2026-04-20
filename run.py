from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

notes = []

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes_page():
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'new')

    if request.method == 'POST':
        text = request.form.get('note')

        if text and text.strip():
            notes.append({
                "text": text.strip(),
                "time": datetime.now().strftime("%H:%M %d-%m-%Y"),
                "important": False
            })

        return redirect('/notes')

    # keep original index (IMPORTANT FIX)
    indexed_notes = list(enumerate(notes))

    # search
    if search:
        indexed_notes = [
            (i, n) for i, n in indexed_notes
            if search.lower() in n["text"].lower()
        ]

    # sorting
    if sort == "old":
        indexed_notes = indexed_notes[::-1]
    elif sort == "important":
        indexed_notes = sorted(indexed_notes, key=lambda x: x[1]["important"], reverse=True)

    return render_template("notes.html",
                           notes=indexed_notes,
                           total=len(notes),
                           search=search,
                           sort=sort)


@app.route('/edit/<int:index>', methods=['POST'])
def edit_note(index):
    updated = request.form.get('note')
    if 0 <= index < len(notes) and updated:
        notes[index]["text"] = updated.strip()
    return redirect('/notes')


@app.route('/delete/<int:index>')
def delete_note(index):
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect('/notes')


@app.route('/important/<int:index>')
def toggle_important(index):
    if 0 <= index < len(notes):
        notes[index]["important"] = not notes[index]["important"]
    return redirect('/notes')


@app.route('/clear')
def clear_notes():
    notes.clear()
    return redirect('/notes')


if __name__ == '__main__':
    app.run(debug=True)