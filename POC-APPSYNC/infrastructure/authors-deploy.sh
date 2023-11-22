#!/bin/bash
region="us-east-1"
account_id="022875025186"

terraform apply -auto-approve -target module.authors_api_image_registry

cd ../authors-api

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $account_id.dkr.ecr.us-east-1.amazonaws.com

docker build -t authors-api .

docker tag authors-api:latest $account_id.dkr.ecr.us-east-1.amazonaws.com/authors-api:latest

docker push $account_id.dkr.ecr.us-east-1.amazonaws.com/authors-api:latest

cd -

terraform apply -auto-approve -target module.app_runner_authors_api