from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os  # <- обязательно импорт

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://inara_user:umdAyKaHjQ2az04ZkGTKHVmS3z65vCaC@dpg-d2r0ejje5dus73cm6bc0-a/inara?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Инициализация базы ---
db = SQLAlchemy(app)


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    relation = db.Column(db.String(100), nullable=False)  # кем является
    attending = db.Column(db.Boolean, nullable=False)     # придет ли

    def __repr__(self):
        return f"<Guest {self.name}>"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add_guest', methods=['POST'])
def add_guest():
    name = request.form['name']
    phone = request.form['phone']
    relation = request.form['relation']
    attending = request.form['attending'] == "yes"  # если выбрали "да"

    new_guest = Guest(name=name, phone=phone, relation=relation, attending=attending)
    db.session.add(new_guest)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
