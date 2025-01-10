#!/bin/sh

if ! command -v ssh-agent > /dev/null; then
  echo "ssh-agent not found. Installing openssh-client..."
  apt-get update && apt-get install -y openssh-client
fi

eval $(ssh-agent -s)

# add the private key
echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -

# debug: list added identities
ssh-add -l

# ssh directory and permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

ssh-keyscan $REMOTE_IP >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

# check if target directory exists on the remote server
ssh $REMOTE_USER@$REMOTE_IP "mkdir -p /home/m320964/library_management"

# Transfer the docker-compose file
scp docker-compose.production.yml $REMOTE_USER@$REMOTE_IP:/home/m320964/library_management/


ssh $REMOTE_USER@$REMOTE_IP "
    echo \"$CI_REGISTRY_PASSWORD\" | docker login -u \"$CI_REGISTRY_USER\" --password-stdin $CI_REGISTRY &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/user_management_service:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/frontend:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/notification_service:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/catalog_management_service:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/reservation_service:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/loan_service:latest:latest &&
    docker pull ${CI_REGISTRY}/library_management_system-group05/custom_nginx:latest &&
    docker compose -f ~/library_management/docker-compose.production.yml up -d --force-recreate
"
