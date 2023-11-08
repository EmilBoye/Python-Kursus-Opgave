from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Åbn en databaseforbindelse og udfør en SELECT-forespørgsel
    conn = sqlite3.connect('PoliceNote.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PoliceMan')
    notes = cursor.fetchall()
    # Luk databaseforbindelsen
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_notes():
    if request.method == 'POST':
        officer_name = request.form['officer_name']
        reason = request.form['reason']
        thought = request.form['thought']

        # Åbn forbindelsen til databasen med en with-sætning for korrekt håndtering af lukning
        with sqlite3.connect('PoliceNote.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PoliceMan (Officer_name, Reason, Thought) VALUES (?, ?, ?)', (officer_name, reason, thought))
            conn.commit()  # Gem ændringerne til databasen

        return redirect(url_for('index'))  # Viderefør til startsiden efter indsættelse

    return render_template('add_notes.html')

@app.route('/update/<int:id>', methods=['GET', 'POST', 'PUT'])
def update_note(id):
    if request.method == 'GET':
        # Hent den eksisterende note baseret på note-id
        conn = sqlite3.connect('PoliceNote.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PoliceMan WHERE Id = ?', (id,))
        note = cursor.fetchone()
        conn.close()

        if note:
            return render_template('update_note.html', note=note)
        else:
            return 'Note not found', 404  # Returner en fejl 404, hvis note ikke findes

    elif request.method in ['POST', 'PUT']:
        officer_name = request.form['officer_name']
        reason = request.form['reason']
        thought = request.form['thought']

        # Opdater noten i databasen baseret på note-id
        conn = sqlite3.connect('PoliceNote.sqlite3')
        cursor = conn.cursor()
        cursor.execute('UPDATE PoliceMan SET Officer_name = ?, Reason = ?, Thought = ? WHERE Id = ?', (officer_name, reason, thought, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST','DELETE'])
def delete_note(id):
    if request.method in ['POST','DELETE']:
        conn = sqlite3.connect('PoliceNote.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f'delete from PoliceMan where Id={id}')
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
