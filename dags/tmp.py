from scripts.download_data import download_data, preprocess_data
from scripts.train_model_rf import train_model as train_model_rf
from scripts.train_model_svm import train_model as train_model_svm
from scripts.train_model_xgb import train_model as train_model_xgb
from scripts.evaluate_models import evaluate_models
from scripts.upload_model import upload_to_cloud
import os


if __name__ == "__main__":
    # preprocess_data()
    # train_model_rf()
    # train_model_svm()
    # train_model_xgb()
    evaluate_models()
    upload_to_cloud("tmp/best_model.txt")