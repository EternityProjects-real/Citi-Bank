from app import db, User, LoanModel, Userinfo, UserTnx, DigitalMortgage

x = User.query.all()

for i in x:
    print(i)
    
y = LoanModel.query.all()

for i in y:
    print(i)

z = Userinfo.query.all()

for i in z:
    print(i)
    
a = UserTnx.query.all()

for i in a:
    print(i)
    
b = DigitalMortgage.query.all()

for i in b:
    print(i)