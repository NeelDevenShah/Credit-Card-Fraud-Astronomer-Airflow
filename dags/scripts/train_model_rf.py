import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    # Load preprocessed data
    X = pd.read_csv('/tmp/X.csv')
    y = pd.read_csv('/tmp/y.csv')

    # Train the model
    model = RandomForestClassifier()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, '/tmp/model_rf.pkl')
