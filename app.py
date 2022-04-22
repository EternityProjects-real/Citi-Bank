from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
from datetime import datetime
import ref_model as ref
from random import randint as rint


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
    name = db.Column(db.String(512), nullable = False)
    password = db.Column(db.String(512), nullable = False)
    account_num = db.Column(db.String(512), nullable = False)
    loan = db.relationship('LoanModel', backref = 'user', lazy = True)
    user_info = db.relationship('Userinfo', backref = 'user', lazy = True)
    user_tnx_info = db.relationship('UserTnx', backref = 'user', lazy = True)
    digitalMortgage = db.relationship('DigitalMortgage', backref = 'user', lazy = True)
    ## Name, password

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
    tnx_id = db.Column(db.String(512), nullable = False)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ## loan amt and loan duration
    
    def __repr__(self):
        return "Id: " + str(self.id) + "Name: " + str(self.name) + ",Amount: " + str(self.loan_amt)

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bank_balance = db.Column(db.Float, nullable = False)
    no_of_transactions = db.Column(db.Float, nullable = False)
    phn_no = db.Column(db.Float,nullable = False)
    address = db.Column(db.Text, nullable = False)
    tnx_id = db.Column(db.String(512), nullable = False)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ## img, ph, add
    
    def __repr__(self):
        return "Id: " + str(self.id) + ", User_id" + str(self.user_id)
    
class UserTnx(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    tnx_to = db.Column(db.String(512), nullable = False)
    tnx_from = db.Column(db.Float, nullable = False)
    tnx_amt = db.Column(db.Float,nullable = False)
    tnx_type = db.Column(db.String(512), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __init__(self):
        return "Id: " + str(self.id) + " User Id: " + str(self.tnx_from)
    
class DigitalMortgage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    mortgage_type = db.Column(db.String(512), nullable = False)
    assest_link = db.Column(db.String(512), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return "Id: " + str(self.id)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods = ['GET', 'POST'])
def index_home():
    return render_template('index2.html')

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', current_user = current_user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user_password = ref.SHA256(user_password)
        pos_users = User.query.filter_by(user_name = user_name)

        for i in pos_users:
            if i.user_name == user_name and i.user_password == user_password:
                user = User.query.get(i.id)
                load_user(user.id)
                login_user(user)
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user_password = ref.SHA256(user_password)
        acct_num = ref.SHA256(str(user_name) + str(user_password))
        user = User(name = user_name, password = user_password, account_num = acct_num)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/signout', methods = ['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update', methods=['GET' ,'POST'])
@login_required
def update():
    if request.method == 'POST':
        userinfo = Userinfo(bank_balance = rint(10000, 10000000000), no_of_transactions = 0.0, phn_no = str(request.form.get('phn_no')), address = str(request.form.get('address')), user_id = current_user.id)
        db.session.add(userinfo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', msg = "An error Happended")

##update +(to) -(from) 
@app.route('/maketnx', methods=['GET' ,'POST'])
@login_required
def maketnx():
    if request.method == 'POST':
        if float(request.form.get('tnx_from')) == current_user.account_num: 
            tnx_info = UserTnx(tnx_to = request.form.get('tnx_to'),tnx_from = request.form.get('tnx_from'),tnx_amt = float(request.form.get('tnx_amt')),tnx_type = str(request.form.get('tnx_type')),user_id = current_user.id)
            db.session.add(tnx_info)
            db.session.commit()
            return render_template('tnx.html', msg = "Tnx successfully ")
    return render_template('tnx.html', msg = "An error Happended")

@app.route('/api/info/user', methods = ['GET'])
@login_required
def api_info_user():
    if request.method == 'GET':
        return jsonify(current_user)
    return("Request Denied")


@app.route('/api/info/userinfo', methods = ['GET'])
@login_required
def api_info_Userinfo():
    if request.method == 'GET':
        return jsonify(current_user.user_info)
    return("Request Denied")


@app.route('/api/info/loan', methods = ['GET'])
@login_required
def api_loan():
    if request.method == 'GET':
        return jsonify(current_user.loan)
    return("Request Denied")

@app.route('/api/info/digitalmortgage', methods = ['GET'])
@login_required
def digitalortgage_info():
    if request.method == 'GET':
        return jsonify(current_user.digitalMortgage)
    return("Request Denied")

@app.route('/api/info/usertnx', methods = ['GET'])
@login_required
def usertnx_info():
    if request.method == 'GET':
        return jsonify(current_user.UserTnx)
    return("Request Denied")

if __name__ == '__main__':
    app.run(debug = True, threaded = True)