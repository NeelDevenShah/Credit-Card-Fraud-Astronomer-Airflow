from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.download_data import download_data, preprocess_data
from scripts.train_model_rf import train_model as train_model_rf
from scripts.train_model_svm import train_model as train_model_svm
from scripts.train_model_xgb import train_model as train_model_xgb
from scripts.evaluate_models import evaluate_models
from scripts.upload_model import upload_to_cloud

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
        op_kwargs={'LOCAL_DATA_PATH':"tmp/creditcard.txt", 'container_client_name': 'gold-data-creditcard', 'blob_name': 'data.zip/creditcard.txt', 'connection_string': 'BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-17T05:04:09Z&st=2024-12-06T21:04:09Z&spr=https,http&sig=zNTxF2JJ8IwSxauhs7RflhzHLmQ5hMgWOQj0wXn07kU%3D'}
    )

    # Preprocessing Task
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        op_kwargs={'LOCAL_DATA_PATH': "tmp/creditcard.txt", 'x_path': 'tmp/X.csv', 'y_path': 'tmp/y.csv', 'x_test_path': 'tmp/X_test.csv', 'y_test_path': 'tmp/y_test.csv'}
    )

    # Train models in parallel
    train_rf_task = PythonOperator(
        task_id='train_random_forest',
        python_callable=train_model_rf,
        op_kwargs={'x_path': 'tmp/X.csv', 'y_path': 'tmp/y.csv'}
    )

    train_svm_task = PythonOperator(
        task_id='train_svm',
        python_callable=train_model_svm,
        op_kwargs={'x_path': 'tmp/X.csv', 'y_path': 'tmp/y.csv'}
    )

    train_xgb_task = PythonOperator(
        task_id='train_xgboost',
        python_callable=train_model_xgb,
        op_kwargs={'x_path': 'tmp/X.csv', 'y_path': 'tmp/y.csv'}
    )

    # Evaluate and select the best model
    evaluate_models_task = PythonOperator(
        task_id='evaluate_models',
        python_callable=evaluate_models,
        op_kwargs={'x_test_path': 'tmp/X_test.csv', 'y_test_path': 'tmp/y_test.csv', 'best_model_write_path': 'tmp/best_model.txt'}
    )
    
    # upload the best model to azure
    upload_models = PythonOperator(
        task_id='upload_model',
        python_callable=upload_to_cloud,
        op_kwargs={'LOCAL_MODEL_PATH': 'tmp/best_model.txt'}
    )
    

    # Task Dependencies
    download_data_task >> preprocess_data_task >> [train_rf_task, train_svm_task, train_xgb_task] >> evaluate_models_task >> upload_models