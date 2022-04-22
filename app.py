from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json 
import ref_model as ref


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
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    loan = db.relationship('LoanModel', backref = 'user', lazy = True)
    user_info = db.relationship('Userinfo', backref='user', lazy = True)

    def __repr__(self):
        return "Id: " + str(self.id) + "Name: " + self.name + " Email: " + self.email

class LoanModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(512), nullable = False)
    loan_amt = db.Column(db.Float, nullable = False)
    loan_amt_paid = db.Column(db.Float, nullable = False)
    loan_amt_percent = db.Column(db.Float, nullable = False)
    loan_duration = db.Column(db.Float, nullable = False)
    loan_paid_time = db.Column(db.String(256), nullable = False)
    loan_type = db.Column(db.String(256), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    

    def __repr__(self):
        return "Id: " + str(self.id) + "Name: " + str(self.name) + ",Amount: " + str(self.loan_amt)
    

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bank_balance = db.Column(db.Float, nullable = False)
    no_of_transactions = db.Column(db.Float, nullable = False)
    img = db.Column(db.String(255),nullable = False)
    phn_no = db.Column(db.String(15),nullable = False)
    father_name = db.Column(db.String(50), nullable = False)
    mother_name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return "Id: " + str(self.id) + ", User_id" + str(self.user_id)

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
        user_password = ref.SHA256(user_password)
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
        user_password = ref.SHA256(user_password)
        Buser = User(name = user_name, password = user_password)
        db.session.add(Buser)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/signout', methods = ['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/info', methods = ['GET', 'POST'])
def api_info():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')

@app.route('/api/info2', methods = ['GET', 'POST'])
def api_info_2():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')

@app.route('/api/info3', methods = ['GET', 'POST'])
def api_info_3():
    if request.method == 'POST':
        something = request.form.get('something')
        something = request.form.get('something')
        something = request.form.get('something')
        ##do something
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, threaded = True)