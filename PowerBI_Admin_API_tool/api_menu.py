import api_get_calls as api_get_calls
import dotenv
import requests




#### TO_DO ####
## Dodać menu # <done
## dodać interfejs okienkowy
## dodać funkcje dodawania użytkownika do datasetu / workspace jako Admin   


def menu():

    while True:
        print("\n#############################")

        print("Possible Data to retrive: ")
        print("\n1. Workspace Info")
        print("2. Workspaces List")
        print("3. Dataset Info")
        print("4. Datasets List")
        print("5. Report Info")
        print("6. Reports List")
        print("7. Dataflow Info")
        print("8. Dataflows List")
        print("9. Scan Workspace for entities")
        print("0000. <in preparation next steps>")

        print("\nX. Exit")
        
        print("#############################")

        chosen_action = input('\nWhat data you want to retrive?: \n').strip()

        if chosen_action == "1":
            api_get_calls.get_workspace_info_by_id()
        elif chosen_action =="2":
            api_get_calls.get_list_of_workspaces()    
        elif chosen_action =="3":
            api_get_calls.get_dataset_info_by_id()
        elif chosen_action =="4":
            api_get_calls.get_list_of_datasets()
        elif chosen_action =="5":
            api_get_calls.get_report_info_by_id()
        elif chosen_action =="6":
            api_get_calls.get_list_of_reports()
        elif chosen_action =="7":
            api_get_calls.get_dataflow_info_by_id()
        elif chosen_action =="8":
            api_get_calls.get_list_of_dataflows()
        elif chosen_action =="9":
            api_get_calls.get_entities_in_specified_workspace()

        elif chosen_action in ["X", "x"]:
            print("Thx for all.")
            break

        else: 
            print("\n >>>>> Invalid choice. Try again.")

menu()