from app import db, User, LoanModel, Userinfo, UserTnx, DigitalMortgage
import pandas as pd

def main():
    return True

def create_user_info(id):
    x = User.query.get_or_404(id)
    tnx_his = x.user_tnx_info
    tnxs = []
    for i in tnx_his:
        tnxs.append(i.tnx_amt)
    
    df = pd.DataFrame(tnxs)
    
    return df, sum(tnxs)
    
        
if __name__ == '__main__':
    main()