#This file is used to make IaC elements. This is used to shorten commands, declare true commands that are written in shell

IMAGE ?= northwind-delivery
TAG   ?= local
NS    ?= northwind
PORT  ?= 8000

.PHONY: help venv install test cov run docker-build docker-run \
        tf-init tf-plan tf-apply tf-destroy k8s-deploy k8s-status \
        k8s-url k8s-delete clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install test dependencies
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

test: ## Run the automated test suite
	python -m pytest

cov: ## Run tests with coverage
	python -m pytest --cov=app --cov-report=term-missing

run: ## Run the service locally
	PORT=$(PORT) python -m app

docker-build: ## Build the container image
	docker build -t $(IMAGE):$(TAG) .

docker-run: ## Run the container and expose on Port number
	docker run --rm -p $(PORT):8000 --name northwind $(IMAGE):$(TAG)

tf-init: # Initialise Terraform (
	terraform -chdir=terraform init

tf-apply: # Provision the namespace adn configmap with terraform
	terraform -chdir=terraform apply -auto-approve

tf-destroy: # Tear down the Terraform-managed environment
	terraform -chdir=terraform destroy -auto-approve

k8s-deploy: # Apply the Kubernetes Deployment and service
	kubectl apply -k k8s

k8s-status: # Show workload status
	kubectl -n $(NS) get deploy,po,svc

k8s-url: # Port-forward the Service to localhost:$(PORT)
	kubectl -n $(NS) port-forward svc/northwind-delivery $(PORT):80

k8s-delete: # Remove the Kubernetes workload
	kubectl delete -k k8s --ignore-not-found

clean: # Remove caches
	rm -rf .pytest_cache **/__pycache__ .coverage
