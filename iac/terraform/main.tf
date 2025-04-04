# Ref: https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/blob/master/examples/simple_autopilot_public
# To define that we will use GCP
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.80.0" // Provider version
    }
  }
  required_version = "1.11.1" // Terraform version
}


// Google Compute Engine
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "e2-standard-2"
  zone         = var.zone

  allow_stopping_for_update = true  # Thêm dòng này vào

  boot_disk {
    initialize_params {
      image = var.image
      size  = 50
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata = {
    ssh-keys = var.ssh_keys
  }
}


// Google Kubernetes Engine
provider "google" {
  project     = var.project_id
  region      = var.region
}

// Google Kubernetes Engine
resource "google_container_cluster" "terraform_gke" {
  name     = "${var.project_id}-gke"
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "my-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.terraform_gke.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n2-standard-8" # 2 CPU and 8 GB RAM
    metadata = {
      ssh-keys = "longvudang:${file("~/.ssh/id_rsa.pub")}"
    }

  }
}



# resource "google_compute_firewall" "firewall_mlops1" {
#   name          = var.firewall_name
#   network = "default"
#   allow {
#     protocol = "tcp"
#     ports = ["8081", "50000", "22"]
#   }
#   source_ranges = ["0.0.0.0/0"]
# }
