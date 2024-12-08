import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerapp import ContainerAppsManagementClient

def deploy_best_model():
    with open('tmp/best_model.txt', 'r') as f:
        best_model_file = f.read().strip()

    # Prepare Docker image
    os.system(f"docker build -t best_model_api:latest .")
    os.system("docker push neeldevenshah/credit_card_best_model_api:latest")

    # Deploy to Azure Container Apps
    credential = DefaultAzureCredential()
    client = ContainerAppsManagementClient(credential, "<your_subscription_id>")
    
    client.container_apps.begin_create_or_update(
        "<resource_group>",
        "best-model-api",
        {
            "location": "East US",
            "properties": {
                "configuration": {
                    "ingress": {"external": True, "targetPort": 5000},
                },
                "template": {
                    "containers": [{
                        "image": "<your_dockerhub_repo>/best_model_api:latest",
                        "name": "best-model-api",
                        "resources": {"cpu": 0.5, "memory": "1Gi"},
                    }],
                },
            },
        },
    )
