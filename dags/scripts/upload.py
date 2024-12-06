from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd

# TODO
def upload_data(LOCAL_DATA_PATH = "/tmp/creditcard.txt", container_client_name='new-container', blob_name='data.zip/creditcard.txt', connection_string='BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-17T05:04:09Z&st=2024-12-06T21:04:09Z&spr=https,http&sig=zNTxF2JJ8IwSxauhs7RflhzHLmQ5hMgWOQj0wXn07kU%3D'):
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container_client_name)
    blob_client = container_client.get_blob_client(blob_name)
    with open(LOCAL_DATA_PATH, "rb") as file:
        blob_client.upload_blob(file)
