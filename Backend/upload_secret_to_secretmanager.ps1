<#
PowerShell helper to upload a service account JSON to Google Secret Manager.
Usage:
  .\upload_secret_to_secretmanager.ps1 -ServiceAccountPath 'C:\path\to\sa.json' -SecretName 'tts-credentials' -Project 'e-to-audio-book'
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$ServiceAccountPath,

    [Parameter(Mandatory=$false)]
    [string]$SecretName = 'tts-credentials',

    [Parameter(Mandatory=$false)]
    [string]$Project = 'e-to-audio-book'
)

# Ensure gcloud is installed and authenticated
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "gcloud CLI not found in PATH. Install Google Cloud SDK first."
    exit 1
}

# Set project
gcloud config set project $Project

# Create secret if it doesn't exist
try {
    gcloud secrets describe $SecretName --project=$Project | Out-Null
} catch {
    Write-Output "Creating secret: $SecretName"
    gcloud secrets create $SecretName --replication-policy="automatic" --project=$Project
}

# Add a new version with the service account JSON file
Write-Output "Uploading $ServiceAccountPath as a new secret version..."
gcloud secrets versions add $SecretName --data-file="$ServiceAccountPath" --project=$Project
Write-Output "Done. Remember to revoke any old keys in the Cloud Console."
