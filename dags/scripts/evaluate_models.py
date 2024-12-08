import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
import os

def evaluate_models(x_test_path='tmp/X_test.csv', y_test_path='tmp/y_test.csv', best_model_write_path='tmp/best_model.txt'):

    def print_folder_contents(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                print(os.path.join(root, file))

    current_directory = os.getcwd()
    print_folder_contents(current_directory)
    
    X_test = pd.read_csv(x_test_path)
    y_test = pd.read_csv(y_test_path)

    model_files = ['tmp/model_rf.pkl', 'tmp/model_svm.pkl', 'tmp/model_xgb.pkl']
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
    with open(best_model_write_path, 'w') as f:
        f.write(best_model_file)
