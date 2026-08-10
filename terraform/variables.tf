variable "kubeconfig_path" {
  description = "Path to the kubeconfig for the local cluster."
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "kubeconfig context of the single-node local cluster (e.g. minikube, k3s, docker-desktop)."
  type        = string
  default     = "docker-desktop"
}

variable "namespace" {
  description = "Namespace the delivery service runs in."
  type        = string
  default     = "northwind"
}

variable "app_port" {
  description = "Port the service listens on inside the container."
  type        = number
  default     = 8000
}

variable "app_environment" {
  description = "Logical environment name surfaced to the running app."
  type        = string
  default     = "local"
}
