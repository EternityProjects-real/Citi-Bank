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
    bank_balance = db.Column(db.Float, nullable = False)
    assest_balance = db.Column(db.Float, nullable = False)
    password = db.Column(db.String(512), nullable = False)
    account_num = db.Column(db.String(512), nullable = False)
    no_of_transactions = db.Column(db.Float, nullable = False)
    loan_assest_balance = db.Column(db.Float, nullable = False)
    loan = db.relationship('LoanModel', backref = 'user', lazy = True)
    user_info = db.relationship('Userinfo', backref = 'user', lazy = True)
    user_tnx_info = db.relationship('UserTnx', backref = 'user', lazy = True)
    digitalMortgage = db.relationship('DigitalMortgage', backref = 'user', lazy = True)
    ## Name, password

    def __repr__(self):
        return "Id: " + str(self.id) + "Name: " + self.name + " Bank Balance: " + str(self.bank_balance)
class LoanModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(512), nullable = False)
    loan_amt = db.Column(db.Float, nullable = False)
    loan_amt_paid = db.Column(db.Float, nullable = False)
    loan_amt_percent = db.Column(db.Float, nullable = False)
    loan_duration = db.Column(db.Float, nullable = False)
    loan_type = db.Column(db.String(256), nullable = False)
    tnx_id = db.Column(db.String(512), nullable = False)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ## loan amt and loan duration
    
    def __repr__(self):
        return "Id: " + str(self.id) + "Name: " + str(self.name) + ",Amount: " + str(self.loan_amt)

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    phn_no = db.Column(db.Float,nullable = False)
    address = db.Column(db.Text, nullable = False)
    age = db.Column(db.String(512), nullable = False)
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
    tnx_id = db.Column(db.String(512), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __init__(self):
        return "Id: " + str(self.id) + " User Id: " + str(self.tnx_from)
    
class DigitalMortgage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    mortgage_type = db.Column(db.String(512), nullable = False)
    assest_link = db.Column(db.String(512), nullable = False)
    estimated_amount = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return "Id: " + str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods = ['GET', 'POST'])
def index():
    if current_user:
        return render_template('index.html', current_user = current_user, val = True)
    return render_template('index.html', current_user  = False)


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
                return render_template('index.html', current_user = current_user, msg = "Loged in!!", val = True)
                

    return render_template('Sign_up.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user_password = ref.SHA256(user_password)
        acct_num = ref.SHA256(str(user_name) + str(user_password))
        user = User(name = user_name, password = user_password, account_num = acct_num, bank_balance = float(rint(10000,100000)), no_of_transactions = 0, assest_balance = 0.0, loan_assest_balance = 0.0)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
        

    return render_template('Sign_up.html')


@app.route('/signout', methods = ['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update', methods=['GET' ,'POST'])
@login_required
def update():
    if request.method == 'POST':
        userinfo = Userinfo(phn_no = str(request.form.get('phn_no')), address = str(request.form.get('address')), age = str(request.form.get('age')),user_id = current_user.id)
        db.session.add(userinfo)
        db.session.commit()
        return render_template('index.html', current_user = current_user, msg = "Updated!!", val = True)
    return render_template('index.html', msg = "An error Happended")

##update +(to) -(from) 
@app.route('/maketnx', methods=['GET' ,'POST'])
@login_required
def maketnx():
    if request.method == 'POST':
        tnx_to = request.form.get('tnx_to')
        tnx_from = request.form.get('tnx_from')
        tnx_amt = float(request.form.get('tnx_amt'))
        tnx_type = "Sending Money"
        tnx_type_to = "Reciving Money"
        
        if str(request.form.get('tnx_from')) == current_user.account_num:
            
            pos_users = User.query.filter_by(account_num = tnx_from)
            
            for i in pos_users:
                if i.account_num == tnx_from:
                    user_to = User.query.get(i.id)
            
            user_to.no_of_transactions += 1
            user_to.bank_balance -= tnx_amt
            
            current_user.no_of_transactions += 1
            current_user.bank_balance -= tnx_amt
            tnx_id = ref.SHA256(tnx_to + tnx_from + tnx_amt + tnx_type + tnx_type_to)
            
            tnx_info = UserTnx(tnx_to = tnx_to ,tnx_from = tnx_from,tnx_amt = tnx_amt,tnx_type = tnx_type, tnx_id = tnx_id, user_id = current_user.id)
            tnx_info_to = UserTnx(tnx_to = tnx_to, tnx_from = tnx_from, tnx_amt = tnx_amt, tnx_type = tnx_type_to, tnx_id = tnx_id, user_id = user_to.id)
            
            db.session.add(tnx_info)
            db.session.add(tnx_info_to)
            db.session.commit()
            
            return render_template('index.html', msg = "Tnx successfully ", val = True)
    return render_template('index.html', msg = "An error Happended")


@app.route('/applylaon', methods = ['GET', 'POST'])
@login_required
def applylaon():
    if request.method == 'POST':
        loan_amt = request.form.get('loan_amt')
        loan_amt_percent = request.form.get('loan_amt_percent')
        loan_duration = request.form.get('loan_duration')
        loan_type = request.form.get('loan_type')
        if current_user.assest_balance <= current_user.loan_assest_balance:
            return render_template('index.html',current_user = current_user, msg = "Asset balance less than loan amount!")
        tnx_id = ref.SHA256(loan_amt + loan_amt_percent + loan_duration + loan_type)
        ##put in the nessary checks
        
        loanModel = LoanModel(name = current_user.name, loan_amt = loan_amt, loan_amt_paid = 0.0, loan_amt_percent = loan_amt_percent, loan_duration = loan_duration, loan_type = loan_type, tnx_id = tnx_id, user_id = current_user.id)
        
        current_user.loan_assest_balance += float(loan_amt)
        
        db.session.add(loanModel)
        db.session.commit()
        return render_template('index2.html', msg = "Loan applied!!", val = True)    
    return render_template('index2.html')



@app.route('/digitalAssestinfo')
@login_required
def digitalAssestinfo():
    if request.method == 'POST':
        mortgage_type = request.form.get('mortgage_type')
        assest_link = request.form.get('assest_link')
        estimated_amount = request.form.get('estimated_amount')
        
        migitalmortgage = DigitalMortgage(mortgage_type = mortgage_type, assest_link = assest_link, estimated_amount = estimated_amount, user_id = current_user.id)
        
        current_user.assest_balance += estimated_amount
        
        db.session.add(migitalmortgage)
        db.session.commit()
        return render_template('index2.html', msg = "Uploaded Successfully", val = True)
    return render_template('index2.html')


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
def digitalmortgage_info():
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