import pandas as pd
from xgboost import XGBClassifier
import joblib

def train_model(x_path='/tmp/X.csv', y_path='/tmp/y.csv'):
    # Load preprocessed data
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path)

    # Train the XGBoost model
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X, y)

    # Save the model
    joblib.dump(model, '/tmp/model_xgb.pkl')
