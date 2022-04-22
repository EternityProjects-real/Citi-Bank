from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json 


with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"] 

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    info = db.relationship('Userinfo', backref='user', lazy=True)

    def __repr__(self):
        return self.name

class Model(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filed1 = db.Column(db.String(512), nullable = False)
    filed2 = db.Column(db.String(512), nullable = False)
    filed3 = db.Column(db.String(512), nullable = False)
    filed4 = db.Column(db.String(256), nullable = False)
    filed5 = db.Column(db.String(512), nullable = False)

    def __repr__(self):
        return str(self.id) + " " + self.filed1
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods = ['GET', 'POST'])
def index_home():
    return render_template('index.html')


@app.route('/home', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        pos_users = User.query.filter_by(user_name = user_name)

        for i in pos_users:
            if i.user_name == user_name and i.user_password == user_password:
                Buser = User.query.get(i.id)
                load_user(Buser.id)
                login_user(Buser)
                return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        Buser = User()
        db.session.add(Buser)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/signout', methods = ['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/info', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')

@app.route('/api/info2', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')

@app.route('/api/info3', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, threaded = True)