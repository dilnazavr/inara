from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Подключение к базе данных Render ---
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://inara_user:umdAyKaHjQ2az04ZkGTKHVmS3z65vCaC@dpg-d2r0ejje5dus73cm6bc0-a/inara?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Инициализация базы ---
db = SQLAlchemy(app)

# --- Модель таблицы Guest ---
class Guest(db.Model):
    __tablename__ = 'guest'  # <- явно задаем имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    relation = db.Column(db.String(100), nullable=False)
    attending = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Guest {self.name}>"

# --- Главная страница ---
@app.route('/')
def index():
    return render_template("index.html")

# --- Добавление гостя ---
@app.route('/add_guest', methods=['POST'])
def add_guest():
    name = request.form['name']
    phone = request.form['phone']
    relation = request.form['relation']
    attending = request.form.get('attending') == "yes"

    new_guest = Guest(name=name, phone=phone, relation=relation, attending=attending)
    db.session.add(new_guest)
    db.session.commit()

    return redirect('/')

# --- Создание таблиц при первом запуске ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # <-- это создаст таблицу guest
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
