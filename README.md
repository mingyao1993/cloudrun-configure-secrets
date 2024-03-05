# gcp-cloudrun-access-secret-manager

## Pre-requisite
- Helm
- Docker
- Google Artifact Registry

## Environment Variables
```bash
export PROJECT_ID=[PROJECT_ID]
export LOCATION=[LOCATION]
export ARTIFACT_REGISTRY_NAME=[ARTIFACT_REGISTRY_NAME]
export IMAGE_NAME=[IMAGE_NAME]
export SERVICE_ACCOUNT_NAME=[SERVICE_ACCOUNT_NAME]
export COMMIT_SHA=$(git rev-parse --short=8 HEAD)
```

## GCP Service Account
permission for cloud run service account to access secrets in secret manager
```bash
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/secretmanager.secretAccessor"
```

## Secret Manager
create secret name as `my_secret`(show link)


## Build and Push to GAR
```bash
docker build . -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REGISTRY_NAME}/${IMAGE_NAME}:${COMMIT_SHA} --platform linux/amd64
docker push ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REGISTRY_NAME}/${IMAGE_NAME}:${COMMIT_SHA}
```


## Helm Chart
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

## Deploy to Cloud Run
```bash
gcloud run services replace infra/service.yaml
```
