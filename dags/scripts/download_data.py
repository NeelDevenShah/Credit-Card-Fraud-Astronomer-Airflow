from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd

def download_data(**kwargs):
    service_client = BlobServiceClient.from_connection_string("BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sc&sp=rwdlacupiytfx&se=2024-12-17T03:51:26Z&st=2024-12-06T19:51:26Z&spr=https,http&sig=TAw3NvQr0pLHsHcphJ%2FXTOfCGlHF9TX5LBC3G9sYxgw%3D")
    container_client = service_client.get_container_client("newexperiment/gold-data-creditcard")
    blob_name = kwargs['blob_name']
    blob_client = container_client.get_blob_client(blob_name)
    with open(LOCAL_DATA_PATH, "wb") as file:
        file.write(blob_client.download_blob().readall())

def preprocess_data(**kwargs):
    df = pd.read_csv(LOCAL_DATA_PATH)
    df.dropna(inplace=True)  # Example preprocessing step
    X = df.drop(columns=['target'])
    y = df['target']
    X.to_csv('/tmp/X.csv', index=False)
    y.to_csv('/tmp/y.csv', index=False)