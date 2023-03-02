import gspread
from google.oauth2.service_account import Credentials #Import google auth and sheets libraries

SCOPE = [ 
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ] #scope for our APIs

CREDS = Credentials.from_service_account_file('creds.json') #Define our credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE) #Define our scope, with credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS) #Pass scope and credentials to our client
SHEET = GSPREAD_CLIENT.open('kuromi_store') #Open our sheet with the client

def get_sales_data():
    """
    Gets the sales figures inputted by the user
    """
    while True:
        print("Please enter the latest sales figures")
        print("Each value should be seperated by a comma as show below")
        print("22,33,44,55")
        data_str = input("Please enter sales figures: ")

        sales_data = data_str.split(',')

        if validate_sales(sales_data):
            break
    return sales_data

        

def validate_sales(values):
    """
    Ensures data is validated before use by checking there are exactly 6 integers provided to us 
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Expected 6 values, got {len(values)}"
            )
    except ValueError as e:
        print (f"Erorr: {e}")
        return False
    
    return True

def update_sales_sheet(data):
    """
    Updates the sales figures on the worksheet
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales data updated!\n")

data = get_sales_data()
sales_data = [int(num) for num in data] #Convert data to integers
update_sales_sheet(sales_data)