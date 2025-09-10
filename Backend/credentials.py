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
  {
  "type": "service_account",
  "project_id": "e-to-audio-book",
  "private_key_id": "a96de7052f983866f1830d577cb60e24ef7c222f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCxo7cXNhLcKzZ1\n6t1D0j4p/Veq0ccdIWLjn6FzdEt690dzPslB7gMd/5JQwsRVxqlo61ncQBTwAteZ\nxujfcOQ6GWW3v6INBnKy0QxJAy6ogRyTPSnNqvH0ksy9Pp5epdTM5MR6Na1kDjqj\npfSvWpTP4DfclEn/K5LFfFVpH0rjNKumrqe7UFUsLBC88UZJQ8u3HEWPz7gwwlQT\n+h9dXOCKH78u7wxaX/FkJrJ/bxKlVR67P1L2ZoHRCyyYcB2/OM3cEzpd9XDE8u3S\nv6vRJA602Brkkd3iYz4/lw1zzHo4T1SSqqjqYfmXfmPr7mMwNEyaxEZXBVtEFcwF\nGRSRcgnZAgMBAAECggEAFJiNPWE1HZbbCR/yiI8DSx4HAJSy99MrooWbFAZLTBYI\nkDma3wyICv3bSobSebl/Yd1LvWgmpU9HDRrNXD68D2prazsKQGVbfhUTzhFS4xGZ\nLQ8d3i0wQXGV0GlGtmWWvyzVBPBdSqkFrnyq2nvvngx6nZYJ4E5+hWwtgPMyXRZI\nBm8Xlbh01WZVnUhSr5fbcUY0eGRwsS+5Gtp4GwjJvgf27jtMTsuRyjCxKj7lZMsY\nd1/0L77JE43+LFgfZl/CJt+Ab91VwFncbeUoSOI964R5RHzhoIyjCLgk6mA/+q54\nA+7wT8hjlW4syriefwVMNMmVTTHVnMW125bMKuHbSQKBgQDtZvwV3hFGIYHKZKQn\nCicHa23nBVeHFRGTj6VGmIl3ENjDoLRGce7JLdso3UNODmELctcD5egnyFmTHQJi\nS0cvMgunfDUumveLSdlxWRYtbP/M6tir/KaSUzpMF1CHK2N4tieBb/aVnOQz5gsK\nskssDj910YdrFihGLA8nt7eSDQKBgQC/jjXLiE9uQcLIzxBLVXb9XQ+Gh1baFJWj\nTesPD8IEqPFgHb60hTWwmc03+AwCdOAfIE0Z9f8kGavuiksOXcDItLikeRTI8CGH\nxXj6zwa6MMUxOLy2NCkRsP421zKTWpjsEen0IDjoxwvrolFWySY3xqAzw+7xn+BU\nF9mjNou//QKBgBtoPkYQAxKDn8ZL5B+VrnfO0TtQhJBVwFe2x6/kwEn8qem7zdQs\nJxMWtix7jt+eDVoTAfuzOSAOozi2qqXKZwdt0aaeUk11Gor8FZxeWo8X/Fgd7LG+\nU0SlUx+huWxBeBRhgyIQWPlgyX+sWS3882y8oFrru6SDRFcFkyJUtV6pAoGALZT+\nkhc2p4r4eeZj/zkwHmxFpIKSFUTusrR46dWbGpbFEVUiqzxDoWmH3vikivUa2+1I\ny5OxCfsd4Z6A68M9e8UdZu31FzelEvTXq/8Vn7q5QdQ5e7X/y9jtNUmSHGRjnVFJ\n9bCxOhsbaA/xARDOilk2h/ro4hBkRj6CqIbzTFUCgYARlYYzjY4Pdwd0mot1b7Bo\nQlZ3ihZBVFx5ibH/g7FMu9AR1N0isLXQLCKaGnEZuDP3IK0rWRkuyb7LlU2o/ATG\nE7PDk7dgEfZSL3BuTNYJFcZ+3Bj5/GERrRZYH5YYpKpQWbd+l9UXof65TKoODj9m\nEGwGqXJlO7Tv4usv7UsSdA==\n-----END PRIVATE KEY-----\n",
  "client_email": "chirp-tts-service-account@e-to-audio-book.iam.gserviceaccount.com",
  "client_id": "117415334017385685529",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/chirp-tts-service-account%40e-to-audio-book.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
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
