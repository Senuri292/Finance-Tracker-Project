import json
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Global list to store transactions
transactions = None

# function to load the json file into a dictionary
def load_transactions():
    # define variable dict_data
    dict_data = None
    try:
        #read the json file
        with open("finance_tracker.json", "r") as file:    

            try:
                dict_data = json.load(file)
            # Handle json decoding error
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    # Handle File Not Found Error 
    except FileNotFoundError:
        # if file not found create a new file
        with open("finance_tracker.json", "w") as file:
            json.dump(dict_data, file)

    #return the dictionary            
    return dict_data

#function to save transaction values into the file   
def save_transactions(transactions):
    #defining data_dict variable
    data_dict = load_transactions()

    # if data_dict is empty then assing transactions to data_dict
    if data_dict is None:
        data_dict = transactions
    #else update data_dict    
    else:
        data_dict.update(transactions)
        

    # rewriting the file with updated data_list
    with open("finance_tracker.json", "w") as file:
        json.dump(data_dict, file)
        
#function to read json file
def read_bulk_transactions_from_file(filename):
    dictionary = None
    #open and read the json file
    with open(filename, "r") as file:
        try:
            dictionary = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        
        if dictionary == None:
            # if json file is empty print a appropriate message to the user
            print("File is Empty")         

    return dictionary
# Handle Value Error for float inputs 
def float_input(message, error_message = "Invalid input!! Please enter a float value."):
    while True:
        try:
            number = float(input(message))
        except ValueError:
            print(error_message)
        else:
            return number

# Handle Value Error for string inputs
def str_input(message, error_message = "Invalid input!! Please enter a string value."):
    while True:
        try:
            text = str(input(message))
        except ValueError:
            print(error_message)
        else:
            return text

# Handle Value Error for integer inputs
def int_input(message, error_message = "Invalid input!! Please enter an integer value."):
    while True:
        try:
            integer = int(input(message))
        except ValueError:
            print(error_message)
        else:
            return integer


# Function to Make sure Income and Expences are the only given answers for varible - amount_type  
def income_and_expenses(error_message = "ERROR!! Please choose from Income or Expenses"):
    choice =  str_input("Choose the type (Income/ Expenses): ")
    while True:
        if (choice.lower() == "Income".lower()):
            return choice
        elif (choice.lower() == "Expenses".lower()):
            return choice
        else:
            # if choice value is not either Income or Expences display appropriate message and get input again
            print(error_message)
            choice =  str_input("Choose the type (Income/ Expenses): ")

# Handle format mistakes for date with datetime module       
def date_input(message, error_message = "Invalid Input!! Please try again."):
    # get user input
    date = input(message)
    while True:
        try:
            # convert string value to datetime object
           date = datetime.datetime.strptime(str(date), "%Y-%m-%d").date()
        except ValueError:
            # if date is not formatted correctly ask the user input again
            print(error_message)
            date = input(message)
        else:
            # return date as string value
            return str(date)
            
# Function to get new values 
def add_transaction():
    transactions = load_transactions()
    # get values from the user
    amount = float_input("Enter the amount: ")
    description = str_input("Enter a short description: ")
    amount_type = income_and_expenses()
    date = date_input("Enter the date in (YYYY-MM-DD) format: ")
    
    # insert inputs into a dictionary
    if (transactions is None):
            #if transactions is empty transactions is equal to new data
            transactions = {description:[{"amount": amount, "date":date}]}
            
    else:
            #if description key already exist add new transactions to existing key
            if description in transactions:
                transactions[description].append({"amount": amount, "date":date})

            else:
                #if description key doesn't exist add new transactions directly to dictionary
                transactions[description] = [{"amount": amount, "date":date}]

    
    # update the dictionary through save_transactions() function
    save_transactions(transactions)
    print("Transaction added Successfully")
    
# Function to view the file    
def view_transactions():
    
    print("--------------------------Transaction log------------------------------------")
    # read data in json file in bulk format
    json_data = read_bulk_transactions_from_file("finance_tracker.json")
    #if json data exist print
    if json_data != None:
        print(json_data)

#function to handle mistakes when entering the key     
def key():
    search_key_dict = load_transactions()
    key_list = search_key_dict.keys()
    print(f"Description list : {key_list}")

    while True:
        #if key exist return key
        key = str_input("Enter the description of the value you want to update/delete(choose from the list above): ")
        if key in key_list:
            break
        
        #if key doesn't exist display an error message 
        else:
            print("Description does not exist!! Please enter a value from description list")

    return key


# function to update and replace given transaction
def update_transaction():
    # assign file to updated_dict variablle
    updated_dict = load_transactions()
    update_key = key()

    while True:
        
        if (len(updated_dict[update_key]) == 1):
            index = 1
            break

        else:
            #get the index from the user
            index = int_input("Enter the number of the transaction you want to update (ex: 1,2,3....): ")
                    
            if (1 > len(updated_dict[update_key])) or (index > len(updated_dict[update_key])):
                # if index does not exist in the nested list print appropriate message
                print("Index does not exist!! Please try again")

            else:
                # if index exist end the loop and return the index
                break
    # get the updated values fron user
    print("Enter the updated values below") 

    amount = float_input("Enter the amount: ")
    amount_type = income_and_expenses()
    date = date_input("Enter the date in (YYYY-MM-DD) format: ")

     
    updated_dict[update_key][index - 1] = {"amount": amount, "date":date}

    # save the updated nested list to json file
    save_transactions(updated_dict)

    print(f"Transaction of the key {update_key} in index {index - 1} updated to {{amount: {amount}, date:{date}}} succesfully!!")

# function to delete values from file
def delete_transaction():
    # assign file to deleted_dict variablle
    deleted_dict = load_transactions()
    delete_key = key()

    while True:
        # if only one transaction exist for the key delete the key value pair
        if (len(deleted_dict[delete_key]) == 1):
            del deleted_dict[delete_key]
            with open("finance_tracker.json", "w") as file:
                json.dump(deleted_dict, file)
            print(f"Transaction for key {delete_key} deleted successfully!!")
            break

        else:
            
            #get the index from the user
            index = int_input("Enter the number of the transaction you want to delete (ex: 1,2,3....): ")
                    
            if (1 > len(deleted_dict[delete_key])) or (index > len(deleted_dict[delete_key])):
                # if index does not exist in the nested list print appropriate message
                print("Index does not exist!! Please try again")

            else:
                # if index exist end the loop and return the index
                del deleted_dict[delete_key][index - 1]
                print(f"Transaction for key {delete_key} in index {index - 1} deleted successfully!!")
                break
    
    # save the changed nested list to json file 
    save_transactions(deleted_dict)

# function to display a summary of transactions    
def display_summary():
    # assign file to final_dict variablle
    final_dict = load_transactions()
    
    totals = {}
    # add the amount values of every description key
    for key, transaction_list in final_dict.items():
        key_sum = 0

        for transaction in transaction_list:
            key_sum += transaction["amount"]
        
        totals[key] = key_sum

    print("-----------------------------SUMMARY--------------------------------")
    print(f"Your total values are {totals}")

def GUI():
    print("Launching Personal Finance Tracker GUI")
    class FinanceTrackerGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Personal Finance Tracker")
            self.create_widgets()
            self.transactions = self.load_transactions("finance_tracker.json")
    
        def create_widgets(self):
            # Search bar and button
            self.search_entry = ttk.Entry(self.root)
            self.search_entry.pack()
        
            self.search_button = ttk.Button(self.root, text="Search", command=lambda:self.search_transactions()) 
            self.search_button.pack()
        
            # Frame for table and scrollbar
            frame = ttk.Frame(self.root, relief=tk.GROOVE)
            frame.pack()

            # Treeview for displaying transactions
            #list of column headings
            columns = ("Description","Amount","Date")
            self.table = ttk.Treeview(frame, columns=columns, show="headings")
            # link the table with sort_by_column function
            for col in columns:
                self.table.heading(col, text=col, command=lambda col=col: self.sort_by_column(col, False))
            self.table.heading("Description", text="Description")
            self.table.heading("Amount", text="Amount")
            self.table.heading("Date", text="Date")
            self.table.pack(side="left")

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
            scrollbar.pack(side="right", fill="y")
            self.table.configure(yscrollcommand=scrollbar.set)

        def load_transactions(self, filename):
            try:
                # read the json file
                with open(filename, "r") as file:
                    try:
                        data = json.load(file)
                    # Handle json decoding error
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
            #if file not found display a message
            except FileNotFoundError:
                print(f"File Not Found!!")
            return data

        #function to display transactions in a table
        def display_transactions(self, transactions):
            transactions = self.load_transactions("finance_tracker.json")
            #creating global lists to store values
            global amountlist, datelist, keys        
            amountlist = []
            datelist = []
            keys = []
                
            # Remove existing entries
            for record in self.table.get_children():
                self.table.delete(record)
    
            # Add transactions to the treeview
            keylist = transactions.keys()
            for key in keylist:
                for transaction in transactions[key]:
                    amountlist.append(str(transaction["amount"]))
                    datelist.append(transaction["date"])
                    keys.append(key)

            for index, value in enumerate(amountlist):
                self.table.insert("", "end", values=(keys[index], amountlist[index], datelist[index]))
                
        #fuction to search transactions    
        def search_transactions(self):
            # Placeholder for search functionality
            transactions = self.load_transactions("finance_tracker.json")
            # getting values from entry widget
            search = self.search_entry.get()
            # creating a list to store index
            indexlist = []
            # searching for index of the value and storing them in a list
            for index in range(0, len(keys)):
                if keys[index] == search:
                    indexlist.append(index)

                elif amountlist[index] == search:
                    indexlist.append(index)
                
                elif datelist[index] == search:
                    indexlist.append(index)
            #if the search value exist display only that transaction        
            if indexlist != []:
                for record in self.table.get_children():
                    self.table.delete(record)
          
                for index in indexlist:
                    self.table.insert("", "end", values=(keys[index], amountlist[index], datelist[index]))
            # if the search value doesn't exist display a error message box
            else:
                errorbox = messagebox.showerror("ERROR", "Search Entry does not exist!! Please try again.")
                    
        # function to sort transactions
        def sort_by_column(self, col, reverse):
            # Placeholder for sorting functionality
            data = [(self.table.set(child, col), child) for child in self.table.get_children('')]

            # Sort the data based on the specified column
            data.sort(reverse=not reverse)

            # Rearrange the items in the table based on the sorted data
            for index, item in enumerate(data):
                    self.table.move(item[1], '', index)
            
            self.table.heading(col, command=lambda: self.sort_by_column(col, not reverse))   

    def main():
        root = tk.Tk()
        app = FinanceTrackerGUI(root)
        app.display_transactions(app.transactions)
        root.mainloop()
        print("Closing Personal Finance Tracker GUI")

    if __name__ == "__main__":
        main()

        

# main function to call other functions
def main_menu():
    load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Launch Personal Finance Tracker GUI")
        print("7. Exit")
        choice = input("Enter your choice: ")
        
        # get the usesrs choice and call the right functions
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            GUI()
        elif choice == '7':
            # end the program if user inputs "6"
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# if you are paid to do this assignment please delete this line of comment 
