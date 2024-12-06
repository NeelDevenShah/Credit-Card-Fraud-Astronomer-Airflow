import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

def evaluate_models():
    X_test = pd.read_csv('/tmp/X_test.csv')
    y_test = pd.read_csv('/tmp/y_test.csv')

    model_files = ['/tmp/model_rf.pkl', '/tmp/model_svm.pkl', '/tmp/model_xgb.pkl', '/tmp/model_nn.pkl']
    best_accuracy = 0
    best_model_file = ""

    for model_file in model_files:
        model = joblib.load(model_file)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        if acc > best_accuracy:
            best_accuracy = acc
            best_model_file = model_file

    # Save best model info
    with open('/tmp/best_model.txt', 'w') as f:
        f.write(best_model_file)
