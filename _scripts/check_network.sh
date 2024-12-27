#!/bin/bash

NETWORK_NAME="glados-network"

if ! docker network ls | grep -q $NETWORK_NAME; then
  echo "Network $NETWORK_NAME not found. Creating..."
  docker network create $NETWORK_NAME
  echo "Network $NETWORK_NAME created successfully."
else
  echo "Network $NETWORK_NAME already exists."
fi