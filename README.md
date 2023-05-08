# Google Cloud Function Template

python 3.10

## Install Python Library

```shell
pip install jsonpickle
pip install functions-framework
pip install google-cloud-firestore
```

## Init GCP

- [Create a Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts)

```
gcloud auth login
gcloud config set project PROJECT_ID

# enable service (for new project and only first time)
gcloud services enable run.googleapis.com

# setup key for debugging
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/gcf-template/function/project-python3/project-000000-000000000000.json"
export GCP_PROJECT="project-000000"
```

## Debug

```shell
./debug.sh
```

## Deploy

```shell
./deploy.sh
```

