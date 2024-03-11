import os

from fastapi import FastAPI, Request
from google.cloud import secretmanager

# API instantiation
app = FastAPI(title="gcp-cloudrun-access-secret-manager")


def get_secret_from_env_var() -> str:
    return os.getenv('my_secret')


def get_secret_from_volume_mount() -> str:
    with open("/secrets/my_secret", "r") as file:
        file_contents = file.read()
    return file_contents


def get_secret_from_api() -> str:
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

    return payload


@app.post("/get_my_secret", status_code=200)
def get_my_secret(request: Request):
    env_var_secret = get_secret_from_env_var()
    print(f"Secret value from env var: {env_var_secret}")

    volume_mount_secret = get_secret_from_volume_mount()
    print(f"Secret value from volume mount: {volume_mount_secret}")

    api_secret = get_secret_from_api()
    print(f"Secret value from API: {api_secret}")

    return {"status_code": 200}
