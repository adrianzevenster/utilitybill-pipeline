variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "region-naam"
}

variable "members" {
  description = "List of users or service accounts to bind roles to"
  type        = list(string)
}