#!/bin/bash

pushd function/project-python3

gcloud functions deploy function_name_1 \
    --gen2 \
    --runtime=python310 \
    --region=us-west1 \
    --source=. \
    --env-vars-file=.env.yaml \
    --entry-point=entrypoint \
    --trigger-http \
    --allow-unauthenticated

popd

