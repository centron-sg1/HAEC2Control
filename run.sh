#!/bin/sh

export AWS_ACCESS_KEY_ID=$(jq -r '.aws_access_key_id' /data/options.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.aws_secret_access_key' /data/options.json)

python3 /app/app.py
