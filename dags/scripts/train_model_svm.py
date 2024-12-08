import pandas as pd
from sklearn.svm import SVC
import joblib

def train_model(x_path='tmp/X.csv', y_path='tmp/y.csv'):
    # Load preprocessed data
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path)

    # Train the SVM model
    model = SVC(probability=True)
    model.fit(X, y)

    # Save the model
    joblib.dump(model, 'tmp/model_svm.pkl')
