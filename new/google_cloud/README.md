# create google cloud storage

Steps to Set Up Google Cloud Storage
Create a Google Cloud Project:

Go to the Google Cloud Console.
Create a new project.
Enable Google Cloud Storage API:

Navigate to the APIs & Services section.
Search for and enable the Cloud Storage API for your project.
Create a Storage Bucket:

Go to the Cloud Storage section.
Create a new bucket and configure it (e.g., set permissions and a unique bucket name).
Set Up Service Account:

In the IAM & Admin section, create a Service Account.
Assign the Storage Object Admin role to this account.
Generate a key for the service account (in JSON format) and download it to your machine.
Install Required Node.js Package:

Run this command to install the Google Cloud Storage client library:
bash

