from hashlib import sha256
import make_data as md
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error as mse

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def predict_model(current_user, id, x_test, y_test):
    df, total_tnxs = md.create_user_info(id)
    x_train = df.iloc[:, :-1].values
    y_train = df.iloc[:, 1].values
    regr = LinearRegression()
    regr.fit(x_train, y_train)
    y_pred = regr.predict(x_test)
    return y_pred, mse(y_pred, y_test), r2_score(y_pred, y_test)


def main():
    print("Ref Model working fine")    
    
if __name__ == "__main__":
    main()