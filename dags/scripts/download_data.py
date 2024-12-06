from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd

LOCAL_DATA_PATH = "/tmp/creditcard.txt"

def download_data():
    service_client = BlobServiceClient.from_connection_string("BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-17T05:04:09Z&st=2024-12-06T21:04:09Z&spr=https,http&sig=zNTxF2JJ8IwSxauhs7RflhzHLmQ5hMgWOQj0wXn07kU%3D")
    blob_name = 'data.zip/creditcard.txt'
    container_client = service_client.get_container_client("gold-data-creditcard")
    blob_client = container_client.get_blob_client(blob_name)
    with open(LOCAL_DATA_PATH, "wb") as file:
        file.write(blob_client.download_blob().readall())

def preprocess_data():
    df = pd.read_csv()
    df.dropna(inplace=True)  # Example preprocessing step
    X = df.drop(columns=['target'])
    y = df['target']
    X.to_csv('/tmp/X.csv', index=False)
    y.to_csv('/tmp/y.csv', index=False)