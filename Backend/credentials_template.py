"""
Google Cloud Credentials Template
Copy this file to credentials.py and add your service account credentials
"""

def get_credentials():
    """
    Return your Google Cloud service account credentials as a dictionary.
    
    Option 1: Return service account JSON as dictionary
    """
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
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    return credentials

    """
    Option 2: Use environment variable for JSON file path
    """
    # import os
    # import json
    # 
    # credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    # if credentials_path:
    #     with open(credentials_path, 'r') as f:
    #         return json.load(f)
    # return None

    """
    Option 3: Return None to use Application Default Credentials
    """
    # return None