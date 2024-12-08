from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd

def upload_to_cloud(LOCAL_MODEL_PATH, blob_name='model.pkl', container_client_name='new-container', connection_string='BlobEndpoint=https://newexperiment.blob.core.windows.net/;QueueEndpoint=https://newexperiment.queue.core.windows.net/;FileEndpoint=https://newexperiment.file.core.windows.net/;TableEndpoint=https://newexperiment.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-17T05:04:09Z&st=2024-12-06T21:04:09Z&spr=https,http&sig=zNTxF2JJ8IwSxauhs7RflhzHLmQ5hMgWOQj0wXn07kU%3D'):
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container_client_name)
    blob_client = container_client.get_blob_client(blob_name)
    
    best_model_file = ""
    with open(LOCAL_MODEL_PATH, 'r') as f:
       best_model_file = f.read()
       
    upload_date = datetime.now().strftime("%Y-%m-%d")
    blob_with_date_name = f'{blob_name}_{upload_date}'
    latest_name = 'latest_version.txt'
    with open(latest_name, 'w') as f:
        f.write(blob_name)
    
    
    with open(best_model_file, "rb") as file:
        blob_client.upload_blob(file, overwrite=True)
        
    with open(latest_name, "rb") as file2:
        blob_client.upload_blob(file2, overwrite=True)