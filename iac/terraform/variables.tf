// Variables to use accross the project
// which can be accessed by var.project_id
variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "bright-seer-452604-f6"
}

variable "region" {
  description = "The region the cluster in"
  default     = "us-central1"
}

variable "zone" {
  description = "The region the cluster in"
  default     = "us-central1-a"
}

variable "bucket" {
  description = "GCS bucket for MLE course"
  default     = "mle-course123123"
}

variable "ssh_keys" {
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDCjbKBi/erW6gMNcE6c8ZN+/sM6tGxwkhyUimfOt9/JRsbTIMDIqlshAs8nn51iJJCsmMbBhmfnNR8b8iA1lgyfsRziES/lGxVRI0pjX8bTXdf3Y4jAucE7oSbWFv20/LyP1CKiJvNO9aZxAptMG5jzhnSoaiPn17vrcgVVQ2dzDBva0HCBNLlQ6EL1V98v+XQLgqKglOdh8bh20a6Z/SdP9QGSatGEN98bnPlATW0/gOviPpzGqwCFbpqvWgTHsfcwntHeUt1TXehF3KhJLZNLTgYYHFRq3Z3Z5GXf9wL+jyoogM/UNnMB/7eFkehgIMUDbjZqn5mCtNdNG+92+50mlGtC12fZVnXVPfG7Bo0C8HW3hojb4tYdg5OxZ0+4TSolbg1Srl/k+5Ciz3/ZsAz66e9LG8dt28s5GymdGiSSmYFtBhu4pqQPd0rYZYbPv2JuYEXZ6iXdiXMvXujd3RGk+UMCCr+jaVE0OWgFJIce7MJIJ3GixrR3pdiKiS0cKs= longvudang@192.168.12.102"
}

variable "firewall_name" {
  description = "Name of firewall"
  default     = "allow-jelkins-port"
}

variable "disk_size" {
  description = "Boot disk size in GB"
  type        = number
  default     = 50
}

variable "image" {
  description = "OS image for the VM"
  type        = string
  default     = "projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230727"
}