from flask import Blueprint, render_template, request, redirect, url_for
from .models import Note
from .utils import filter_notes, sort_notes

main = Blueprint('main', __name__)

notes = []


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/notes', methods=['GET', 'POST'])
def notes_page():
    try:
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'new')

        if request.method == 'POST':
            text = request.form.get('note')

            if text and text.strip():
                notes.append(Note(text.strip()))

            return redirect(url_for('main.notes_page'))

        # Prepare notes
        indexed_notes = list(enumerate(notes))

        indexed_notes = filter_notes(indexed_notes, search)
        indexed_notes = sort_notes(indexed_notes, sort)

        return render_template(
            'notes.html',
            notes=indexed_notes if indexed_notes else [],
            total=len(notes),
            search=search,
            sort=sort
        )

    except Exception as e:
        print("ERROR in /notes:", e)
        return "<h2>Internal Error - Check Terminal</h2>"


@main.route('/edit/<int:index>', methods=['POST'])
def edit(index):
    if 0 <= index < len(notes):
        text = request.form.get('note')
        if text and text.strip():
            notes[index].text = text.strip()

    return redirect(url_for('main.notes_page'))


@main.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(notes):
        notes.pop(index)

    return redirect(url_for('main.notes_page'))


@main.route('/important/<int:index>')
def important(index):
    if 0 <= index < len(notes):
        notes[index].important = not notes[index].important

    return redirect(url_for('main.notes_page'))


@main.route('/clear')
def clear():
    notes.clear()
    return redirect(url_for('main.notes_page'))


# 🔥 DEBUG ROUTE (VERY IMPORTANT)
@main.route('/debug')
def debug():
    return f"""
    <h3>Debug Info</h3>
    <p>Total Notes: {len(notes)}</p>
    <p>Notes List: {notes}</p>
    """