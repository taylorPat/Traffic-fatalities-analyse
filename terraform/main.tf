terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.29.0"
    }
  }
}

provider "google" {
  credentials = file("${var.GOOGLE_APPLICATION_CREDENTIALS}")
  project     = "${var.GCP_PROJECT_ID}"
  region      = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.GCP_BUCKET_NAME
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id    = "${var.GCP_BQ_DATASET}"
  friendly_name = "test"
  description   = "This is a test description"
  location      = var.location
}