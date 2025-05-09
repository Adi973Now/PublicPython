## jedyny działający sposób



import requests
from dotenv import load_dotenv
import os
from azure.identity import InteractiveBrowserCredential
 

load_dotenv()

# Replace these with your actual values
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
api_url = 'https://api.powerbi.com/v1.0/myorg/admin/groups?$top=100'
scope = ['https://analysis.windows.net/powerbi/api/.default']
 
# Create an InteractiveBrowserCredential instance
credential = InteractiveBrowserCredential(tenant_id=tenant_id)
 
# Acquire a token
token = credential.get_token(*scope).token
 
# Get the list of workspaces
headers = {
    'Authorization': f'Bearer {token}'
}
response = requests.get(api_url, headers=headers)
print("Status Code:", response.status_code)
print("Response Text:", response.text)
workspaces = response.json()
 
# Print the list of workspaces
for workspace in workspaces['value']:
    print(f"Workspace ID: {workspace['id']}, Name: {workspace['name']}")

