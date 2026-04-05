from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    pinned = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    notes = Note.query.order_by(Note.pinned.desc()).all()
    return render_template('index.html', notes=notes)



@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']

    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()

    return redirect('/')


@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    note = Note.query.get(id)

    if note:
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()

    return redirect('/')



@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')



@app.route('/pin/<int:id>')
def pin(id):
    note = Note.query.get(id)
    note.pinned = not note.pinned
    db.session.commit()
    return redirect('/')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)