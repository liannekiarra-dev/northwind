output "namespace" {
  description = "Namespace provisioned for the application."
  value       = kubernetes_namespace.app.metadata[0].name
}

output "config_map" {
  description = "Name of the ConfigMap the Deployment consumes via envFrom."
  value       = kubernetes_config_map.app.metadata[0].name
}
