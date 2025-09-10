"""
Google Cloud Credentials Template
Copy this file to credentials.py and add your service account credentials
"""

def get_credentials():
    """
    Return your Google Cloud service account credentials as a dictionary. 
    
    Option 1: Return service account JSON as dictionary
    Option 2: Use environment variables 
    Option 3: Use Google Secret Manager
    """
    
    # Option 1: Service Account JSON (NOT RECOMMENDED for production)
    # Replace with your actual service account credentials
    credentials = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id", 
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    # Option 2: Use environment variables (RECOMMENDED)
    # import os
    # import json
    # credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    # if credentials_json:
    #     return json.loads(credentials_json)
    
    # Option 3: Use Google Secret Manager (BEST for production)
    # from google.cloud import secretmanager
    # client = secretmanager.SecretManagerServiceClient()
    # name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    # response = client.access_secret_version(request={"name": name})
    # return json.loads(response.payload.data.decode("UTF-8"))
    
    return credentials

# Alternative: Use Application Default Credentials (ADC)
def get_credentials_adc():
    """
    Use Google Application Default Credentials.
    This is the most secure method for production.
    """
    # Just return None and let Google Cloud libraries handle authentication
    return None
