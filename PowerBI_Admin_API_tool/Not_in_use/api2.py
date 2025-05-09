#### to nie działa


import requests
import json
from msal import PublicClientApplication

# === CONFIGURATION ===
tenant_id = "your-tenant-id"
client_id = "your-client-id"  # Must be a registered app in Azure AD
workspace_id = "087bf472-d460-4b00-bbdf-b68cc94dae36"
user_to_add = "Azadmin-ADRN@ecco.onmicrosoft.com"

# === AUTHENTICATION ===
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://analysis.windows.net/powerbi/api/.default"]

app = PublicClientApplication(client_id, authority=authority)

# Interactive login (use device code flow)
result = app.acquire_token_interactive(scopes=scopes)

if "access_token" in result:
    token = result["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # === API CALL: Add user as Admin ===
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/users"
    payload = {
        "identifier": user_to_add,
        "principalType": "User",
        "accessRight": "Admin"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("User added successfully.")
    else:
        print(f"Failed to add user: {response.status_code} - {response.text}")
else:
    print(f"Authentication failed: {result.get('error_description')}")