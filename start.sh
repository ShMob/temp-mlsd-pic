#!/bin/bash

nginx -g "daemon off;" & mlflow server \
    --backend-store-uri /mlflow_runs \
    --default-artifact-root /mlflow_artifacts \
    --host 0.0.0.0 \
    --port 5000 \
	& uvicorn main:app --host 0.0.0.0 --port 8000