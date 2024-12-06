from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.download_data import download_data, preprocess_data
from scripts.train_model_rf import train_model as train_model_rf
from scripts.train_model_svm import train_model as train_model_svm
from scripts.train_model_xgb import train_model as train_model_xgb
# from scripts.train_model_nn import train_model as train_model_nn
from scripts.evaluate_models import evaluate_models
# from scripts.deploy_container import deploy_best_model
    
# Default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='credit_card_fraud_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # Download data from Azure Blob Storage
    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
    )

    # Preprocessing Task
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    # Train models in parallel
    train_rf_task = PythonOperator(
        task_id='train_random_forest',
        python_callable=train_model_rf,
    )

    train_svm_task = PythonOperator(
        task_id='train_svm',
        python_callable=train_model_svm,
    )

    train_xgb_task = PythonOperator(
        task_id='train_xgboost',
        python_callable=train_model_xgb,
    )

    # train_nn_task = PythonOperator(
    #     task_id='train_neural_network',
    #     python_callable=train_model_nn,
    # )

    # Evaluate and select the best model
    evaluate_models_task = PythonOperator(
        task_id='evaluate_models',
        python_callable=evaluate_models,
    )

    # Deploy the best model to Azure Container Apps
    # deploy_best_model_task = PythonOperator(
    #     task_id='deploy_best_model',
    #     python_callable=deploy_best_model,
    # )

    # Task Dependencies
    download_data_task >> preprocess_data_task >> [train_rf_task, train_svm_task, train_xgb_task] >> evaluate_models_task
    
    # >> deploy_best_model_task
