from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def download_data(LOCAL_DATA_PATH = "tmp/creditcard.txt", container_client_name='gold-data-creditcard', blob_name='data.zip/creditcard.txt', connection_string='BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-17T05:04:09Z&st=2024-12-06T21:04:09Z&spr=https,http&sig=zNTxF2JJ8IwSxauhs7RflhzHLmQ5hMgWOQj0wXn07kU%3D'):
    os.makedirs(os.path.dirname(LOCAL_DATA_PATH), exist_ok=True)
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container_client_name)
    blob_client = container_client.get_blob_client(blob_name)
    with open(LOCAL_DATA_PATH, "wb") as file:
        file.write(blob_client.download_blob().readall())

def preprocess_data(LOCAL_DATA_PATH = "tmp/creditcard.txt", x_path='tmp/X.csv', y_path='tmp/y.csv', x_test_path='tmp/X_test.csv', y_test_path='tmp/y_test.csv'):
    df = pd.read_csv(LOCAL_DATA_PATH)
    df.dropna(inplace=True)  # Example preprocessing step
    X = df.drop(columns=['Class'])
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train.to_csv(x_path, index=False)
    y_train.to_csv(y_path, index=False)
    X_test.to_csv(x_test_path, index=False)
    y_test.to_csv(y_test_path, index=False)
    
    
    def print_folder_contents(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                print(os.path.join(root, file))

    current_directory = os.getcwd()
    print_folder_contents(current_directory)