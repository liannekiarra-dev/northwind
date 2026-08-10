

locals {
  common_labels = {
    "app.kubernetes.io/part-of"    = "northwind-logistics"
    "app.kubernetes.io/managed-by" = "terraform"
  }
}

resource "kubernetes_namespace" "app" {
  metadata {
    name   = var.namespace
    labels = local.common_labels
  }
}

resource "kubernetes_config_map" "app" {
  metadata {
    name      = "northwind-delivery-config"
    namespace = kubernetes_namespace.app.metadata[0].name
    labels    = local.common_labels
  }

  data = {
    PORT            = tostring(var.app_port)
    APP_ENVIRONMENT = var.app_environment
  }
}
