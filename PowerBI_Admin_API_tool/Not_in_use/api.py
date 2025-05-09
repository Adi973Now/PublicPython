import requests
from dotenv import load_dotenv
import os
from azure.identity import InteractiveBrowserCredential
import msal

load_dotenv()

tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET_VALUE_PYTHON')
access_token = os.getenv('ACCESS_TOKEN')


def get_workspace_name(): 

    # Load environment variables from .env file
    load_dotenv()

    # Define the workspace ID and the API endpoint
    workspace_id = input('Provide WorkspaceID: ')
    
    api_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}'

    # Your access token (replace with your actual token)
    access_token = get_access_token()

    # Set up the headers with the authorization token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the GET request to the Power BI API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        workspace_details = response.json()
        workspace_name = workspace_details.get('name')
        print(f'Workspace Name: {workspace_name}')
    else:
        print(f'Failed to retrieve workspace details: {response.status_code}')
        print(response.json())


def get_list_of_workspaces():
    access_token = get_access_token()
    if not access_token:
        return

    api_url = 'https://api.powerbi.com/v1.0/myorg/groups'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        workspaces = response.json().get('value', [])
        for workspace in workspaces:
            print(f"Workspace ID: {workspace['id']}, Workspace Name: {workspace['name']}")
    else:
        print(f'Failed to retrive workspaces: {response.status_code}')
        print(response.json())


def get_access_token():
    
    # Azure AD details
    resource = 'https://analysis.windows.net/powerbi/api'
    authority = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

    # Request payload
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': resource
    }

    # Make the POST request to get the access token
    response = requests.post(authority, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f'Failed to get access token: {response.status_code}')
        try:
            print(response.json())
        except Exception:
            print(response.text)
        return None
'''
    # Check if the request was successful
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print(f'\n >>>>>>>>>>>> Access Token: {access_token}')
    else:
        print(f'\n >>>>>>>>>>>> Failed to get access token: {response.status_code}')
        print(response.json())
'''

def get_access_token2():

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.organization"
    }

    

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to get token:", response.status_code)
        print(response.json())
        return None


def show_access_token():
    access_token = get_access_token2()
    if access_token:
        print(f'\n >>>>>>>>>>>> Access Token: {access_token}')
    else:
        print('\n >>>>>>>>>>>> Failed to get access token.')
    




########## new approach - using delegated scopes, not applications

def abc():

    AUTHORITY = f"https://login.microsoftonline.com/{tenant_id}"
    SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]  # or specific scopes like Workspace.Read.All

    app = msal.PublicClientApplication(client_id, authority=AUTHORITY)

# Step 1: Get device code
    flow = app.initiate_device_flow(scopes=SCOPE)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow")

    print(f"🔑 Go to: {flow['verification_uri']}")
    print(f"🔐 Enter code: {flow['user_code']}")

# Step 2: Wait for login
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        print("\n✅ Access token acquired.")
        token = result['access_token']

        # Use token to call Power BI API
        headers = {
            "Authorization": f"Bearer {result['access_token']}"
        }

# Example: List workspaces
        response = requests.get("https://api.powerbi.com/v1.0/myorg/groups", headers=headers)
        print("\n📦 Workspaces:")
        print(response.json())

    else:
        print("\n❌ Failed to acquire token:", result.get("error_description"))


def main():

    
    while True:
        print("\n#############################")

        print("Possible Data to retrive: ")
        print("\n1. Workspace Name")
        print("2. Workspaces List")
        print("3. Access Token")
        print("4. <in preparation next steps>")

        print("\nX. Exit")
        
        print("#############################")

        chosen_action = input('\nWhat data you want to retrive?: \n').strip()

        if chosen_action == "1":
            get_workspace_name()
        elif chosen_action =="2":
            get_list_of_workspaces()    
        elif chosen_action =="3":
            show_access_token()
        elif chosen_action =="4":
            break
        elif chosen_action in ["X", "x"]:
            print("Thx for all.")
            break

        else: 
            print("\n >>>>> Invalid choice. Try again.")





def test_env():


    print(tenant_id)
    print(client_id)
    print(client_secret)
    print(access_token)    

#####
#main()
abc()
#test_env()
#get_access_token()
#show_access_token()
#get_list_of_workspaces()


