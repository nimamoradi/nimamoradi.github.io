Title: Building a Todo App with GCP: Part 1 - Setting Up Infrastructure
Date: 2024-09-28 10:00
Category: Programming
Tags: python, GCP
Slug: Todo app
Authors: Nima Moradi
Summary: An todo app using GCP tech stack


Welcome to the first part of our journey in building a todo app using the Google Cloud Platform (GCP) tech stack. In this multi-part series, we'll explore how to leverage various GCP services to create a robust and scalable todo application. Our goal is to provide users with the ability to register tasks and receive email notifications when the task due time approaches.

In this initial post, we'll focus on setting up the necessary infrastructure using Terraform and deploying our first Cloud Function to handle adding tasks to Firestore.

## Getting Started with GCP

To begin, make sure you have a GCP account set up. If you haven't already, head over to the <a href="https://console.cloud.google.com/">GCP Console</a> and create a new project.

Next, install the Google Cloud SDK on your local machine. This will allow you to interact with GCP services from the command line. Once installed, initialize the SDK by running:

<pre><code>gcloud init</code></pre>

Follow the prompts to authenticate and select the project you created earlier.

## Defining Infrastructure with Terraform

We'll use Terraform to define and manage our infrastructure as code. This ensures reproducibility and makes it easy to update and maintain our setup.

Here's a look at our Terraform configuration files:

### main.tf

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_firestore_database" "default" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# ... (rest of the configuration)
```

In <code>main.tf</code>, we specify the required providers, including the Google provider. We also define a Firestore database resource to store our todo tasks.

### variables.tf

```hcl
variable "project_id" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

variable "region" {
  description = "The region in which to provision resources."
  type        = string
  default     = "us-central1"
}
```

The <code>variables.tf</code> file defines the input variables for our Terraform configuration, such as the project ID and region.

## Deploying the Cloud Function

To handle adding tasks to Firestore, we'll create a Cloud Function using Python. Here's the code for our function:

```python
import uuid
from google.cloud import firestore
import json

db = firestore.Client()

def add_task(request):
    # ... (function implementation)
    pass
```

The <code>add_task</code> function receives a POST request with the task details and adds it to the Firestore database.

To deploy the Cloud Function, we define the necessary resources in <code>main.tf</code>:

```hcl
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function.zip"
}

resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-bucket"
  location = var.region
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "function-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

resource "google_cloudfunctions_function" "todo_app" {
name = "todo-app"
description = "Todo App Function"
runtime = "python39"

available_memory_mb = 256
source_archive_bucket = google_storage_bucket.function_bucket.name
source_archive_object = google_storage_bucket_object.function_zip.name
trigger_http = true
entry_point = "add_task"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
project = google_cloudfunctions_function.todo_app.project
region = google_cloudfunctions_function.todo_app.region
cloud_function = google_cloudfunctions_function.todo_app.name

role = "roles/cloudfunctions.invoker"
member = "allUsers"
}
```

These resources create a Cloud Storage bucket to store the function code, archive the code into a zip file, and deploy the Cloud Function with the specified configuration. We also grant the "Cloud Functions Invoker" role to all users to allow them to invoke the function.

## Applying the Infrastructure

With the Terraform configuration in place, we can apply the changes to provision the necessary resources. Run the following commands:

<pre><code>terraform init
terraform apply
</code></pre>

Review the execution plan and confirm the changes by typing "yes" when prompted.

Once the infrastructure is provisioned, Terraform will output the URL of the deployed Cloud Function:

```hcl
output "function_url" {
  value       = google_cloudfunctions_function.todo_app.https_trigger_url
  description = "URL of the deployed function"
}
```

You can use this URL to invoke the function and add tasks to your todo app.

## Conclusion
In this first part of the series, we set up the foundation for our todo app using GCP and Terraform. We provisioned a Firestore database to store our tasks and deployed a Cloud Function to handle adding tasks.

In the upcoming parts, we'll explore additional features such as user registration, email notifications, and more. Stay tuned as we continue to build our todo app using the powerful capabilities of GCP!
