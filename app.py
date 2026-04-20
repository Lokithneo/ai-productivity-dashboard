from flask import Flask, render_template, request, redirect

app = Flask(__name__)

notes = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes_page():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            notes.append(note)
    return render_template('notes.html', notes=notes)

@app.route('/delete/<int:index>')
def delete_note(index):
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect('/notes')

if __name__ == '__main__':
    app.run(debug=True)