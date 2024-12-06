import pandas as pd
from xgboost import XGBClassifier
import joblib

def train_model():
    # Load preprocessed data
    X = pd.read_csv('/tmp/X.csv')
    y = pd.read_csv('/tmp/y.csv')

    # Train the XGBoost model
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X, y)

    # Save the model
    joblib.dump(model, '/tmp/model_xgb.pkl')
