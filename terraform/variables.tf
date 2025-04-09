# Set inside ../.env file
variable "GOOGLE_APPLICATION_CREDENTIALS" {
  description = "For authentication with GCP"
}

# Set inside ../.env file
variable "GCP_PROJECT_ID" {
  description = "Project"
}

# Set inside ../.env file
variable "GCP_BQ_DATASET" {
  description = "My BigQuery dataset name"
}

# Set inside ../.env file
variable "GCP_BUCKET_NAME" {
  description = "My Storage Bucket Name"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "region" {
  description = "Project region"
  default     = "europa-west3"
}