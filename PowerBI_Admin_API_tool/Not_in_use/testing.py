#### to nie działa


import requests
import msal
from dotenv import load_dotenv
import os

def get_access_token():
    # Load environment variables from .env file
    load_dotenv()

    # Azure AD details
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    tenant_id = os.getenv('TENANT_ID')
    client_id = os.getenv('CLIENT_ID')

    authority = 'https://login.microsoftonline.com/' + tenant_id
    scopes = ['https://analysis.windows.net/powerbi/api/.default']

    client = msal.PublicClientApplication(client_id, authority=authority)
    response = client.acquire_token_by_username_password(username=username, password=password, scopes=scopes)

    if 'access_token' in response:
        return response['access_token']
    else:
        print(f"Error: {response['error_description']}")
        return None

def abc():
    access_token = get_access_token()
    if access_token:
        # Use the access token to make API requests
        headers = {'Authorization': f'Bearer {access_token}'}
        # Example API request
        url = 'https://api.powerbi.com/v1.0/myorg/reports'
        response = requests.get(url, headers=headers)
        print(response.json())

abc()
