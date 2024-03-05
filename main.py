import os

from fastapi import FastAPI, Request

# API instantiation
app = FastAPI(title="gcp-cloudrun-access-secret-manager")


def get_secret_from_env_var() -> None:
    print(os.getenv('my_secret'))


def get_secret_from_volume_mount() -> None:
    with open('/secrets/my_secret', 'r') as file:
        file_contents = file.read()
    print(file_contents)


def get_secret_from_api() -> None:
    print('get_secret_from_api')


@app.post("/get_my_secret", status_code=200)
def get_my_secret(request: Request):

    get_secret_from_env_var()

    get_secret_from_volume_mount()

    get_secret_from_api()

    return {"status_code": 200}
