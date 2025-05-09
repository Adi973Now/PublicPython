import requests
from dotenv import load_dotenv
import os
from azure.identity import InteractiveBrowserCredential

load_dotenv()

# Replace these with your actual values
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID') 
base_web_url = "https://app.powerbi.com/"
base_admin_url = "https://api.powerbi.com/v1.0/myorg/admin"
scope = ['https://analysis.windows.net/powerbi/api/.default']


#### BASE

def get_access_token():
    try:
        credential = InteractiveBrowserCredential(tenant_id=tenant_id)
        token = credential.get_token(*scope).token
        return token
        
    except Exception as e:
        print(f"[Auth Error] {e}")
        return None
    

### Workspaces

def get_list_of_workspaces():
    top_rows = input("How many workspaces?\n")
    token = get_access_token()

    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/groups?$top={top_rows}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        workspaces = response.json().get("value", [])
        for ws in workspaces:
            print(f"ID: {ws['id']}")
            print(f"Name: {ws['name']}")
            print("-" * 40)

    else:
        print(f"[Error] Could not fetch workspaces: {response.status_code}")
        print(response.text)

def get_workspace_info_by_id():
    workspace_id = input("Enter Workspace ID: \n").strip()
    token = get_access_token()
    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/groups/{workspace_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        name = response.json().get("name")
        print(f"Workspace Name: {name}")
    else:
        print(f"[Error] Workspace not found: {response.status_code}")
        print(response.text)


### Datasets


def get_list_of_datasets():
    top_rows = input("How many datasets?\n")
    token = get_access_token()

    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/datasets?$top={top_rows}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        workspaces = response.json().get("value", [])
        for ws in workspaces:
            print(f"Dataset ID: {ws['id']}")
            print(f"Workspace ID:{ws['workspaceId']}")
            print(f"Name: {ws['name']}")
            print(f"Configured_by: {ws['configuredBy']}")
            print("-" * 40)

    else:
        print(f"[Error] Could not fetch datasets: {response.status_code}")
        print(response.text)



def get_dataset_info_by_id():
    dataset_id = input("Enter Dataset ID: \n").strip()
    token = get_access_token()
    if not token:
        print("[Error] Could not get access token.")
        return
    
    url = f"{base_admin_url}/datasets/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        datasets = response.json().get("value", [])
        target_dataflow = next((d for d in datasets if d["id"] == dataset_id), None)

        if target_dataflow:
            print(f"\nID: {target_dataflow['id']}")
            print(f"Name: {target_dataflow['name']}")
            print(f"Configured By: {target_dataflow['configuredBy']}")
            print(f"Web URL: {target_dataflow.get('webUrl')}")
            print(f"Workspace ID: {target_dataflow.get('workspaceId')}")
        else:
            print(f"[Info] Dataset with ID {dataset_id} not found.")
    else:
        print(f"[Error] Failed to retrieve datasets: {response.status_code}")
        print(response.text)


def test():
    dataflow_id = input("Enter Dataflow ID: \n").strip()
    token = get_access_token()
    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/dataflows/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dataflows = response.json().get("value", [])
        target_dataflow = next((df for df in dataflows if df.get("id") == dataflow_id), None)

        if target_dataflow:
            print(f"\nID: {target_dataflow['id']}")
            print(f"Name: {target_dataflow['name']}")
            print(f"Configured By: {target_dataflow.get('configuredBy', 'N/A')}")
            print(f"Web URL: {target_dataflow.get('webUrl', 'N/A')}")
            print(f"Workspace ID: {target_dataflow.get('workspaceId', 'N/A')}")
        else:
            print(f"[Info] Dataflow with ID {dataflow_id} not found.")
    else:
        print(f"[Error] Failed to retrieve dataflows: {response.status_code}")
        print(response.text)


### Reports
def get_list_of_reports():
    top_rows = input("How many reports?\n")
    token = get_access_token()

    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/reports?$top={top_rows}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reports = response.json().get("value", [])
        print(f"\nFound {len(reports)} reports in the organization:\n")
        
        for rpt in reports:
            print(f"Report ID: {rpt['id']}")
            print(f"Name: {rpt['name']}")
            try:
                print(f"Dataset ID: {rpt['datasetId']}")
            except KeyError:
                print("Dataset ID: [Not Available]")
            print(f"Workspace ID: {rpt['workspaceId']}")
            print(f"Report URL: {rpt.get('webUrl')}")
            print("-" * 40)
    else:
        print(f"[Error] Could not fetch reports: {response.status_code}")
        print(response.text)


def get_report_info_by_id():
    pass


### Dataflows
def get_list_of_dataflows():
    pass


def get_dataflow_info_by_id():
    dataflow_id = input("Enter Dataflow ID: \n").strip()
    token = get_access_token()
    if not token:
        print("[Error] Could not get access token.")
        return
    
    url = f"{base_admin_url}/dataflows/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dataflows = response.json().get("value", [])
        target_dataflow = next((df for df in dataflows if df["id"] == dataflow_id), None)

        if target_dataflow:
            print(f"\nID: {target_dataflow['objectid']}")
            print(f"Name: {target_dataflow['name']}")
            print(f"Configured By: {target_dataflow['configuredBy']}")
            print(f"Web URL: {target_dataflow.get('modelUrl')}")
            print(f"Workspace ID: {target_dataflow.get('workspaceId')}")
        else:
            print(f"[Info] Dataflow with ID {dataflow_id} not found.")
    else:
        print(f"[Error] Failed to retrieve dataflow: {response.status_code}")
        print(response.text)


### Scan Workspace

def get_entities_in_specified_workspace():   

    workspace_id  = input("\nEnter workspace ID you want to scan: \n").strip()

    while True:
        print("\nWhat do you want to get from this workspace?")
        print("\n1. Datasets")
        print("2. Dataflows")
        print("3. Reports")
        print("4. Dashboards")
        #print("4. Users / Groups in this workspace")

        choice = input("\nEnter choice: \n").strip().lower()
        if choice == '1':
            entity_type = 'datasets'
            break
        elif choice == '2':
            entity_type = 'dataflows'
            break
        elif choice == '3':
            entity_type = 'reports'
            break
        elif choice == '4':
            entity_type = 'dashboards'
            break
            ##entity_type = 'users'
            ##print(entity_type)
            ##break
        else:
            print("Invalid option. Try again.")

    print(f"\nShowing  {entity_type}.")

    token = get_access_token()
    if not token:
        print("[Error] Could not get access token.")
        return

    url = f"{base_admin_url}/groups/{workspace_id}/{entity_type}?$top=500"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        entities = response.json().get('value', [])
        
        if entities:
            print(f"\nFound {len(entities)} {entity_type} \nin workspace {workspace_id}:")
            for en in entities:
                if entity_type == 'datasets':
                    print(f"\nDataset ID: {en['id']}")
                    print(f"Name: {en['name']}")
                    print(f"URL: {en.get('webUrl')}")
                    print(f"Configured By: {en.get('configuredBy')}")
                elif entity_type == 'dataflows':
                    print(f"\nDataflow ID: {en['objectId']}")
                    print(f"Name: {en['name']}")
                    print(f"URL: {en.get('modelUrl')}")
                    print(f"Configured By: {en.get('configuredBy')}")
                elif entity_type == 'reports':
                    print(f"\nReport ID: {en['id']}")
                    print(f"\nDataset ID: {en['datasetId']}")
                    print(f"Name: {en['name']}")
                    print(f"URL: {en.get('webUrl')}")
                elif entity_type == 'dashboards':
                    print(f"\nDashboard ID: {en['id']}")
                    print(f"Name: {en['displayName']}")
                    print(f"URL: {base_web_url}/groups/{workspace_id}/{entity_type}/{en['id']}?experience=power-bi")
                else:
                    print("Wrong entity chosen.")
        else:
            print(f"No {entity_type} found in this workspace.")
    else:
        print(f"[Error] Could not fetch {entity_type}: {response.status_code}")
        print(response.text)



## Testing

get_dataflow_info_by_id()

#get_entities_in_specified_workspace()