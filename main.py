import os

from fastapi import FastAPI, Request
from google.cloud import secretmanager

# API instantiation
app = FastAPI(title="gcp-cloudrun-access-secret-manager")


def get_secret_from_env_var() -> None:
    print(f"Secret value from env var: {os.getenv('my_secret')}")


def get_secret_from_volume_mount() -> None:
    with open("/secrets/my_secret", "r") as file:
        file_contents = file.read()
    print(f"Secret value from volume mount: {file_contents}")


def get_secret_from_api() -> None:
    project_id = os.getenv("PROJECT_ID")
    secret_id = "my_secret"
    version_id = "latest"

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret.
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    print(f"Secret value from API: {payload}")


@app.post("/get_my_secret", status_code=200)
def get_my_secret(request: Request):
    get_secret_from_env_var()

    get_secret_from_volume_mount()

    get_secret_from_api()

    return {"status_code": 200}
