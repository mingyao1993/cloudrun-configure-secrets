# GCP Cloud Run Access Secret Manager

This repository demonstrates three methods to securely retrieve secrets from Google Cloud Platform (GCP) Secret Manager
within a Cloud Run service.

## Overview

Cloud Run services often need access to sensitive information stored in GCP Secret Manager.
This repository outlines three approaches to integrate and manage such secrets within your Cloud Run services:

1. **Environment Variables**: Pass secrets directly to the Cloud Run environment for easy access during runtime.

2. **Volume Mounting**: Mount secrets as volumes within the Cloud Run container, making it available as files.

3. **Secret Manager API Requests**: Use the Secret Manager API.

## Pre-requisite

- Helm
- Docker
- Google Artifact Registry

### Environment Variables

Replace placeholders with actual values:

```bash
export PROJECT_ID=[PROJECT_ID]
export LOCATION=[LOCATION]
export ARTIFACT_REGISTRY_NAME=[ARTIFACT_REGISTRY_NAME]
export IMAGE_NAME=[IMAGE_NAME]
export SERVICE_ACCOUNT_NAME=[SERVICE_ACCOUNT_NAME]
export COMMIT_SHA=$(git rev-parse --short=8 HEAD)
```

### GCP Service Account

To create and grant permissions for the Cloud Run service account to access secrets in Secret Manager, run the following
commands:

```bash
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/secretmanager.secretAccessor"
```

### Secret Manager

To follow along with the example provided in this repository, please ensure that you create a secret named my_secret in
the GCP Secret Manager.

You may find this link helpful for creating a secret in the Google Cloud Platform Secret Manager:
[Creating and Accessing Secrets](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets)
.

## Cloud Run Service

To build the Docker image for your Cloud Run service and push it to Google Artifact Registry, run the following
commands:

```bash
docker build . -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REGISTRY_NAME}/${IMAGE_NAME}:${COMMIT_SHA} --platform linux/amd64
docker push ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REGISTRY_NAME}/${IMAGE_NAME}:${COMMIT_SHA}
```

After building and pushing the Docker image, create the Cloud Run service YAML file using the Helm chart:

```bash
helm template charts infra \
--set projectId=${PROJECT_ID} \
--set location=${LOCATION} \
--set artifactRegistryName=${ARTIFACT_REGISTRY_NAME} \
--set imageName=${IMAGE_NAME} \
--set serviceAccountName=${SERVICE_ACCOUNT_NAME} \
--set commitSha=${COMMIT_SHA} \
> infra/service.yaml
```

Finally, deploy the Cloud Run service by executing the following command:

```bash
gcloud run services replace infra/service.yaml
```

Finally, you can trigger the Cloud Run service through methods like HTTP requests or Pub/Sub messages.

## Troubleshooting

For troubleshooting and additional information, please refer to
the [GCP documentation](https://cloud.google.com/run/docs/configuring/services/secrets).