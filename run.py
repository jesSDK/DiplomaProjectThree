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
    print("Please enter the latest sales figures")
    print("Each value should be seperated by a comma as show below")
    print("22,33,44,55")
    data_str = input("Please enter sales figures: ")

    sales_data = data_str.split(',')
    validate_sales(sales_data)

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


get_sales_data()
