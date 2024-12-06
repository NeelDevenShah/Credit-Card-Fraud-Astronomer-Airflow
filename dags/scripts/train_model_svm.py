import pandas as pd
from sklearn.svm import SVC
import joblib

def train_model():
    # Load preprocessed data
    X = pd.read_csv('/tmp/X.csv')
    y = pd.read_csv('/tmp/y.csv')

    # Train the SVM model
    model = SVC(probability=True)
    model.fit(X, y)

    # Save the model
    joblib.dump(model, '/tmp/model_svm.pkl')
