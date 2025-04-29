import os
import sys
from datetime import datetime

patient_dict= {}
nurse_dict = {}
doctor_dict = {}
labtech_dict = {}
item_costs_dict = {"room": 175, "gauze": 25, "consultation": 400, "catheter": 115}
lab_catalog = {"CBC": 25, "CMP": 45, "Lipid Panel": 30, "HbA1c": 25}

#Patient Module
class Patient:
    def __init__(self, patient_id, first_name, last_name, age, address, admit_date, billing_items):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.__age = age 
        self.address = address
        self.admit_date = admit_date
        self.billing_items = billing_items
        self.line_item_costs = {}
        for item in billing_items: #Changed this to list the actual items, not just their costs.
            if item in item_costs_dict:
                self.line_item_costs[item] = item_costs_dict[item]
            elif item not in item_costs_dict:
                self.line_item_costs[item] = 0
        self.total_bill = sum(self.line_item_costs.values()) #This is also updated when labs are added. Medications not added yet (No costs).
        #Meds and Labs - #Added as secondary function, are really only here as a precaution.
        self.medications = []
        self.labs = []
        self.lab_total = 0


    def set_age(self, new_age):
        self.__age = new_age

    def get_age(self):
        return self.__age

    def to_string(self):
        return f"{self.patient_id}, {self.first_name}, {self.last_name}, {self.__age}, {self.address}, {self.admit_date}, {self.billing_items}, {self.line_item_costs}, {self.labs}, {self.lab_total}, {self.medications}, {self.total_bill}"

def new_patient():
    while True:
        patient_id = input("Patient ID (or Q to quit): ").strip()
        if patient_id.lower() == "q":
            print()
            return
        if patient_id in patient_dict:
            print("Duplicate Patient ID, please enter another ID.")
            continue
        else:
            break
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    while True:
        age_input = input("Age: ").strip()
        try:
            age = int(age_input)
            if age < 0 or age > 130:
                print("Please enter a valid age.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for age.")
    address = input("Address: ").strip()
    while True:
        admit_date = input("Admit Date (MM/DD/YYYY): ").strip()
        try:
            datetime.strptime(admit_date, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date format. Use MM/DD/YYYY.")
    billing_items = input("Billing Items as a Comma-Seperated List: ").lower().strip().split(",")
    patient_dict[patient_id] = Patient(patient_id, first_name, last_name, age, address, admit_date, billing_items)

    print(f"Patient account '{patient_id}' created successfully.")
    with open("patients.txt", "a") as file:
        file.write(Patient.to_string(patient_dict[patient_id]) + "\n")
    
    print(f"Patient {first_name} {last_name} has been stored in the file.")

def change_patient_info():
    while True:
        patient_needing_updated_info = input("Enter Patient ID for update or Q to quit: ")
        if patient_needing_updated_info.lower() == "q":
                    print("Exiting Patient Search")
                    break
        if patient_needing_updated_info in patient_dict:
            info_needing_update = input(f""" 
    What info needs to be updated:
    1. First Name
    2. Last Name
    3. Age
    4. Address
    5. Admit Date
    """)
    
            if info_needing_update.strip() == "1":
                new_first_name = input("Enter new First Name: ")
                patient_dict[patient_needing_updated_info].first_name = new_first_name
                print(f"Patient info updated")
            elif info_needing_update.strip() == "2":
                new_last_name = input("Enter new Last Name: ")
                patient_dict[patient_needing_updated_info].last_name = new_last_name
                print(f"Patient info updated")
            elif info_needing_update.strip() == "3":
                new_age = input("Enter new Age: ")
                patient_dict[patient_needing_updated_info].set_age(new_age)
                print(f"Patient info updated")
            elif info_needing_update.strip() == "4":
                new_address = input("Enter new Address: ")
                patient_dict[patient_needing_updated_info].address = new_address
                print(f"Patient info updated")
            elif info_needing_update.strip() == "5":
                new_admit_date = input("Enter new Admit Date: ")
                patient_dict[patient_needing_updated_info].admit_date = new_admit_date
                print(f"Patient info updated")
            else:
                print("Invalid choice")
            
            
            with open("patients.txt", "w") as file:
                for i in patient_dict.values():
                    file.write(i.to_string() + "\n")
        else:
            print("No patient found with that ID. Try again or quit.")
            continue

def display_info_for_patient_view():
    while True:
        id_input = input("Enter Patient ID or Q to quit: ")
        if id_input.lower() == 'q':
                print("Exiting Patient Search")
                print()
                return      
        try:
            active_user = patient_dict[id_input]
        except KeyError:
            print("No patient found. Try again or logout")
            continue
        info = active_user.to_string().split()
        first_name = info[1]
        last_name = info[2]
        print(f"Name: {first_name[0]}***** {last_name[0]}******")
        print("Itemized Bill:")
        for key, value in active_user.line_item_costs.items():
            print(f"   {key.title()} - ${value}")
        if active_user.labs:
            for item in active_user.labs:
                print("   Lab Tests")
                print(f"      {item}")
                print(f"   Lab Total - ${active_user.lab_total}")
        print(f"Total Bill: ${active_user.total_bill}")



#Doctor Module
#Changed this one to be object oriented. I know it might be better to use dicts in modern coding but everythign else
#was OOP so I thought it would be easier.

class Doctor:
    #Initializes class instance based on which user log into the system and uses the attributes associated with that user_id key.
    def __init__(self, user_id, password, first_name, last_name, specialty, phone):
        self.__user_id = user_id
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.phone = phone
    def get_password(self):
        return self.__password
    #Uses the doctor dict to login.        
    def login():
        while True:
            print("\n--- Doctor Login ---")
            print("Please enter your User ID and Password, or Q to quit.")
            user_id = input("User ID: ")
            if user_id.strip().lower() == "q":
                print("Exiting Doctor Login")
                print("--------------------\n")
                print()
                return
            password = input("Password: ")
            if user_id in doctor_dict:
                if doctor_dict[user_id].get_password() == password:
                    print(f"Login successful. Welcome Dr. {doctor_dict[user_id].last_name}")
                    doctor_dict[user_id].doctor_menu()
                    return
                else:
                    print("User ID or Password Incorrect. Try again")
            else:
                print("Invalid user ID. Try again.")

    #Main menu of doctor functions. Tasks 4 and 5 call functions from other modules.
    def doctor_menu(self):
        while True:
            print("\n--- Doctor Menu ---")
            print("1. Create New Account")
            print("2. View Patient Records")
            print("3. Order Labs")
            print("4. Prescribe Medication")
            print("5. Edit Patient Records")
            print("6. Discharge Patient")
            print("7. Logout")
            task = input("Select an option: ")
            if task == "1":
                while True:
                    print("---Account Creator---")
                    print("1. Doctor\n2. Nurse\n3. Patient\n4. Lab Technician\n5. Quit")
                    account_selection = input("Select account type: ")
                    if account_selection.lower().strip() == "1":
                        self.create_doctor()
                    elif account_selection.lower().strip() == "2":
                        make_new_nurse() #Added from Nurse Module
                    elif account_selection.lower().strip() == "3":
                        new_patient() #Added from Patient Module
                    elif account_selection.lower().strip() == "4":
                        make_new_tech() #Added from Lab Tech Module
                    elif account_selection.lower().strip() == "5":
                        print()
                        break
                    else:
                        print("Invalid input, please try again.")
            elif task == "2":
                self.view_patient_details()
            elif task == "3":
                self.order_labs()
            elif task == "4":
                self.prescribe_medication()
            elif task == "5":
                change_patient_info()
            elif task == "6":
                discharge_patient()
            elif task == "7":
                print("Logging out...")
                print()
                return
            else:
                print("Invalid input, please try again.")
    #Adds to the doctor dict.                
    def create_doctor(self):
        while True:
            print("\n--- Create New Account ---")
            user_id = input("New User ID: ")
            if user_id in doctor_dict:
                print("Duplicate Doctor ID, please enter another ID.")
                continue
            else:
                break
        password = input("Password: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        specialty = input("Specialty: ")
        phone = input("Phone number: ")
        doctor_dict[user_id] = Doctor(user_id, password, first_name, last_name, specialty, phone)
        print(f"Doctor account '{user_id}' created successfully.")

    #Uses the instance data to print record report. Used format from the patient and nurse modules.
    def view_patient_details(self):
        while True:
            print("\n--- Patient Details ---")
            patient_details_input = input("Enter Patient ID or Q to quit: ")
            if patient_details_input.strip().lower() == "q":
                print("Exiting Patient Search")
                break
            try:
                target_patient = patient_dict[patient_details_input]
                print(f"Name - {target_patient.last_name},{target_patient.first_name}\nAge - {target_patient.get_age()}\nAddress - {target_patient.address}\nAdmit Date -  {target_patient.admit_date}")
                print("Itemized Bill:")
                for key, value in target_patient.line_item_costs.items():
                    print(f"   {key.title()} - ${value}")
                if target_patient.labs:
                    print("   Lab Tests")
                    for item in target_patient.labs:
                        print(f"    {item}")
                    print(f"   Lab Total - ${target_patient.lab_total}")
                if target_patient.medications:
                    print("   Medications:")
                    for item in target_patient.medications:
                        print(f"    {item["Medication"]}")
                        print(f"      {item["Dosage"]}, {item["Route"]}, {item["Frequency"]}")
                    # med = {"Medication": medication_name, "Dosage": dosage, "Route": route, "Frequency": frequency}
                print(f"Total Bill: ${target_patient.total_bill}")
                break
            except KeyError:
                print("No Patient Found. Try again.")
                continue
        print("--------------------\n")     
    
    #Adds labs and lab_total for cost as new instance variables, and adds their costs to the total bill.
    def order_labs(self):
        while True:
            print("\n--- Order Labs ---")
            pt_id = input("Enter Patient ID or Q to quit: ").strip()
            if pt_id.lower() == "q":
                print("Exiting Patient Search")
                break
            if pt_id not in patient_dict:
                print("Patient ID not found. Please try again.")
                continue
            if pt_id in patient_dict:
                patient = patient_dict[pt_id]
            while True:
                print("\n--- Lab Menu ---")
                for lab, cost in lab_catalog.items():
                    print(f'{lab}: ${cost}')
                lab_select = input("Select Lab or Q to quit: ")
                if lab_select.strip().lower() == "q":
                    print("Closing lab ordering interface.")
                    break
                if lab_select in lab_catalog:
                    patient.labs.append(lab_select)
                    patient.lab_total += lab_catalog[lab_select]
                    patient.total_bill += lab_catalog[lab_select]
                    print(f"{lab_select} ordered for patient {pt_id}.")
                    print(f"New total lab cost: ${patient.lab_total}")
                else:
                    print("Invalid lab selection. Please try again.")
                #Add to persistent storage
                with open("patients.txt", "w") as file:
                    for i in patient_dict.values():
                        file.write(i.to_string() + "\n")

    #Adds a diction of all medication information to the patient instance medication list.
    def prescribe_medication(self):
        print("\n--- Prescribe Medication ---")
        while True:
            pt_id = input("Enter Patient ID or Q to quit: ")
            if pt_id.strip().lower() == "q":
                print("Exiting Patient Search")
                break
            if pt_id in patient_dict:
                patient = patient_dict[pt_id]
                medication_name = input("Medication: ")
                dosage = input("Dosage: ")
                route = input("Route: ")
                frequency = input("Frequency: ")
                med = {"Medication": medication_name, "Dosage": dosage, "Route": route, "Frequency": frequency}
                patient.medications.append(med)
                
                #Add to persistent storage
                with open("patients.txt", "w") as file:
                    for i in patient_dict.values():
                        file.write(i.to_string() + "\n")
                    
                print(f"{medication_name} has been prescribed for Patient ID {pt_id}.")
                break
            else:
                print('No patient found')
                continue

#Nurse Module
class Nurse:
    def __init__(self, user_id, password, first_name, last_name, floor):
        self.__user_id = user_id
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        self.floor = floor
    def get_user_id(self):
        return self.__user_id
    def get_password(self):
        return self.__password
    def get_password_hidden(self):
        hidden_password = ""
        for letter in self.get_password():
            hidden_password += "*"
        return hidden_password
#Uses user_id as the nurse_dict key, and tests the password against the instance password variable. Success calls the nurse menu.    
    def login_nurse():
        print("\n--- Nurse Login ---")
        print("Please enter your User ID and Password, or Q to quit.")
        while True: 
            user_id_input = input("User ID: ")
            if user_id_input.strip().lower() == "q":
                print("Exiting Nurse Login")
                print("--------------------\n")
                print()
                return
            password_input = input("Password: ")
            if user_id_input in nurse_dict:
                active_user = nurse_dict.get(user_id_input)
                if password_input == active_user.get_password():
                    print("Login Accepted")
                    print("--------------------\n")
                    active_user.interface_for_nurse()
                else:
                    print("User ID or Password Incorrect. Try again")
                    continue
            else:
                print("User ID or Password Incorrect. Try again")
                continue
            break
#Menu can allow nurses to make and view patients, and their own account info.
    def interface_for_nurse(self):
        while True:
            print("\n--- Nurse Interface ---")
            print("Welcome to the Nurse Interface")
            print("1. Make New Patient\n2. View Patient Details\n3. Edit Patient Details\n4. Display Nurse Details\n5. Logout")
            interface_input = input("What would you like to do?\n")
            if interface_input == '1':
                self.make_new_patient()
            elif interface_input == '2':
                self.view_patient_details()
            elif interface_input == '3':
                change_patient_info()
            elif interface_input == '4':
                self.display_nurse_info()
            elif interface_input == '5':
                print("--- Closing Interface ---")
                print()
                return
            else:
                print("Invalid Input")
                continue
#Nurse finctions all use patient instanc evariables, but need to be updated to include medications and labs.
    def make_new_patient(self):
        print("\n--- New Patient ---")
        print("Please enter patient information")
        new_patient()
        print("--------------------")
    def display_nurse_info(self):
        print("--- Account Info ---")
        print(f"Name - {self.last_name},{self.first_name}\nUser ID - {self.get_user_id()}\nPassword - {self.get_password_hidden()}\nFloor - {self.floor}")
        print("--------------------")
    def view_patient_details(self):
        while True:
            print("\n--- Patient Details ---")
            patient_details_input = input("Enter Patient ID or Q to quit: ")
            if patient_details_input == 'Q' or patient_details_input == 'q':
                print("Exiting Patient Search")
                break
            try:
                target_patient = patient_dict[patient_details_input]
                print(f"Name - {target_patient.last_name},{target_patient.first_name}\nAge - {target_patient.get_age()}\nAddress - {target_patient.address}\nAdmit Date -  {target_patient.admit_date}")
                print("Itemized Bill:")
                for key, value in target_patient.line_item_costs.items():
                    print(f"   {key.title()} - ${value}")
                if target_patient.labs:
                    print("   Lab Tests")
                    for item in target_patient.labs:
                        print(f"    {item}")
                    print(f"   Lab Total - ${target_patient.lab_total}")
                if target_patient.medications:
                    print("   Medications:")
                    for item in target_patient.medications:
                        print(f"    {item["Medication"]}")
                        print(f"      {item["Dosage"]}, {item["Route"]}, {item["Frequency"]}")
                    # med = {"Medication": medication_name, "Dosage": dosage, "Route": route, "Frequency": frequency}
                print(f"Total Bill: ${target_patient.total_bill}")
                break
            except KeyError:
                print("No Patient Found. Try again.")
                continue
        print("--------------------\n")  
#Function for doctors, adds a new nurse instance to the dictionary.
def make_new_nurse():
    print("Please enter Nurse Profile information")
    while True:
        user_id = input("User ID: ")
        if user_id in nurse_dict:
            print("Duplicate Nurse ID, please enter another ID.")
            continue
        else:
            break
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    floor = input("Floor Number: ")
    nurse_dict[user_id] = Nurse(user_id, password, first_name, last_name, floor)   
    print(f"Nurse account '{user_id}' created successfully.")
# Lab Tech Module


class LabTechnician:
   
    def __init__(self, user_id, password, first_name, last_name):
        self.user_id = user_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


    # Login added 
    def login():
        print("\n--- Lab Technician Login ---")
        print("Please enter your User ID and Password, or Q to quit.")
        while True:
            user_id = input("User ID: ")
            if user_id.strip().lower() == "q":
                print("Exiting Lab Technician Login")
                print("--------------------\n")
                print()
                return
            password = input("Password: ")
            # lab tech user login
            if user_id in labtech_dict:
                if labtech_dict[user_id].password == password:
                    print(f"Login successful. Welcome {labtech_dict[user_id].first_name}!")
                    lab_tech = labtech_dict[user_id]
                    lab_tech.lab_menu()
                    return
            else:
                print("Login failed. Try again.")

   
    # main menu for lab tech module.
    def lab_menu(self):
        while True:
            print("\n--- Lab Technician Menu ---")
            print("1. View Assigned Lab Tests")
            print("2. Edit Lab Test Info")
            print("3. Logout")
            selected_choice = input("Select an option: ")

            if selected_choice == "1":
                self.view_assigned_labs()
            elif selected_choice == "2":
                self.edit_lab_test()
            elif selected_choice == "3":
                print("Returning to main menu...")
                print()
                return
            else:
                print("Invalid choice. Try again.")
   
    def view_assigned_labs(self):
        # views labs for the specific patient by their ID.
        try:
            pid = input("Enter Patient ID or Q to quit: ")
            if pid.strip().lower() == "q":
                return
            if pid in patient_dict:
                patient = patient_dict[pid]
                print(f"\nPatient: {patient.first_name} {patient.last_name}")
                for key, value in patient.line_item_costs.items():
                    print(f"   {key.title()} - ${value}")
                if patient.labs:
                    print("   Lab Tests")
                    for item in patient.labs:
                        print(f"      {item}")
                    print(f"    Lab Total - ${patient.lab_total}")
                if patient.medications:
                    print("   Medications:")
                    for item in patient.medications:
                        print(f"    {item["Medication"]}")
                        print(f"      {item["Dosage"]}, {item["Route"]}, {item["Frequency"]}")
                print(f"Total Bill: ${patient.total_bill}")
            else:
                print("Patient not found.")
        except Exception as e:
            print(f"Error: {e}")

    def edit_lab_test(self):
        try:
            pid = input("Enter Patient ID to edit or Q to quit: ")
            if pid.strip().lower() == "q":
                return
            if pid in patient_dict:
                patient = patient_dict[pid]
                print(f"\nCurrent Lab Info for {patient.first_name} {patient.last_name}:")
                if patient.labs:
                    for item in patient.labs:
                        print("   Lab Tests")
                        print(f"      {item}")
                        print(f"   Lab Total - ${patient.lab_total}")
                else:
                    print("No Labs Assigned")

                new_items = input("Enter new Assigned lab name (comma-separated): ")
                new_cost = int(input("Enter new Assigned lab cost: "))

                # updates bill patient info
                # patient.billing_items = new_items
                # patient.line_item_costs = new_cost
                # patient.total_bill = new_cost + (patient.total_bill - patient.line_item_costs)
                
                ## this part should overwrites the cost in the lab tests instead 
                patient.labs = [lab.strip() for lab in new_items.split(",")]
                patient.lab_total = new_cost
                patient.total_bill = sum(patient.line_item_costs.values()) + patient.lab_total

                # Save updates to file
                with open("patients.txt", "w") as file:
                    for p in patient_dict.values():
                        file.write(p.to_string() + "\n")

        except Exception as e:
            print(f"Error: {e}")

#Function to make a new lab tech
def make_new_tech():
    print("Please enter Lab Technician Profile information")
    while True:
        user_id = input("User ID: ")
        if user_id in labtech_dict:
            print("Duplicate Lab Tech ID, please enter another ID.")
            continue
        else:
            break
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    labtech_dict[user_id] = LabTechnician(user_id, password, first_name, last_name)
    print(f"Lab technician account '{user_id}' created successfully.")

#Exit Module
#Closes out the full program. 
#Currently only accessable from main menu, 
def exit_system():
    print("Exiting HIS. Bye bye! Keep up the amazing work! :)")
    sys.exit()

#Discharge Module

def discharge_patient():
    while True:
        patient_id = input("Patient ID for Discharge or Q to quit: ")
        if patient_id.strip().lower() == "q":
            return
        elif patient_id in patient_dict:
            break
        elif patient_id not in patient_dict:
            print(f"No patient found with ID: {patient_id}")

        

    patient = patient_dict[patient_id]
    filename = f"{patient.first_name.lower()}{patient.last_name.lower()}_discharged.txt"

    # Displaying details
    print("\n--- Discharge Summary ---")
    print(f"Patient ID: {patient_id}")
    print(f"Name: {patient.first_name} {patient.last_name}")
    for key, value in patient.line_item_costs.items():
        print(f"  {key.title()} - ${value}")
    if patient.labs:
        for item in patient.labs:
            print("   Lab Tests")
            print(f"      {item}")
            print(f"   Lab Total - ${patient.lab_total}")
    if patient.medications:
        for item in patient.medications:
            print("  Medications")
            print(f"    Medication: {item["Medication"]}")
            print(f"    Dosage: {item["Dosage"]}")

    print(f"Total Bill: ${patient.total_bill}")
    print("--------------------------")

    # Writing to file
    with open(filename, 'w') as file:
        file.write(f"Patient ID: {patient_id}\n")
        file.write(f"Name: {patient.first_name} {patient.last_name}\n")
        file.write("Itemized Bill:\n")
        for key, value in patient.line_item_costs.items():
            file.write(f"   {key.title()} - ${value}\n")
        if patient.labs:
            print("Lab Tests:\n")
            for item in patient.labs:
                file.write(f"      {item}\n")
        if patient.medications:
            print("Medications:\n")
            for item in patient.medications:
                file.write(f"    Medication: {item["Medication"]}\n")
                file.write(f"    Dosage: {item["Dosage"]}\n")
        file.write(f"   Lab Total - ${patient.lab_total}\n")
        file.write(f"Total Bill: ${patient.total_bill}\n")
    
    if patient_id in patient_dict:
        del patient_dict[patient_id]
        print(f"Patient {patient_id} has been successfully removed.")
        
        # Rewrite the file without the removed patient
        with open("patients.txt", "w") as file:
            for i in patient_dict.values():
                file.write(i.to_string() + "\n")
    else:
        print("No patient found with that ID.")

    # Deleting patient record
    print(f"Patient {patient.first_name} {patient.last_name} has been discharged and the record has been deleted.\nFile saved as {filename}.")

def load_default_users():
    doctor_dict["chief"] = Doctor("chief","1234","Default","Default","Admin","0")
    patient_dict["0001"] = Patient("0001", "Stefan", "Nguyen", "12", "Hell Ave", "04/20/2025", ["catheter", "room"])
    nurse_dict["nurse1"] = Nurse('nurse1', 'password', 'Sasha', 'Patschke', 1)
    doctor_dict["doctor1"] = Doctor("doctor1", "password", "Drew", "Gordon", "Family Medicine", "5127814115")
    labtech_dict["tech1"] = LabTechnician("tech1", "password", "Ari", "Rez")

    
#Main Menu
def open_main_menu():
    while True:
        load_default_users()
        print("Welcome to the Hospital Interface System")
        print()
        print("Sign In As: \n")
        print("1. Patient\n2. Doctor\n3. Nurse\n4. Lab Technician\n5. Exit System")
        while True:
            main_input = input("")
            if main_input == "1":
                display_info_for_patient_view()
            elif main_input == "2":
                Doctor.login()
            elif main_input == "3":
                Nurse.login_nurse()
            elif main_input == "4":
                LabTechnician.login()
            elif main_input == "5":
                exit_system()
            else:
                print("Not an option. Try again.")
                print()
            break

open_main_menu()
