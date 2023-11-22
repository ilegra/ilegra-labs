#!/bin/bash
region="us-east-1"
account_id="022875025186"

terraform apply -auto-approve -target module.books_api_image_registry

cd ../books-api

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $account_id.dkr.ecr.us-east-1.amazonaws.com

docker build -t books-api .

docker tag books-api:latest $account_id.dkr.ecr.us-east-1.amazonaws.com/books-api:latest

docker push $account_id.dkr.ecr.us-east-1.amazonaws.com/books-api:latest

cd -

terraform apply -auto-approve -target module.app_runner_books_api