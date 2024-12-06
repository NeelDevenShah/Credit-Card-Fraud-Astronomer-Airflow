import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model(x_path='/tmp/X.csv', y_path='/tmp/y.csv'):
    # Load preprocessed data
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path)

    # Train the model
    model = RandomForestClassifier()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, '/tmp/model_rf.pkl')
