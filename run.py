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
        print("11,22,33,44,55,66")
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

def calculate_surplus(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    - Positive surplus indicates stock not sold
    - Negative surplus indicates extra ordered when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values() #Get stock values from worksheet
    stock_row = stock[-1] #gives us the last stock entry

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data,worksheet):
    """
    Updates the specified worksheet with new data
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} data updated!")
    
def last_5_sales():
    """
    Gets the last 5 entries for each item available for sale
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock(data):
    """
    Calcuates the average stock for each item and make a recomendationg
    """
    print("Calculating stock data...\n")
    stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        recommended_stock = average * 1.1
        stock_data.append(round(recommended_stock))
    return stock_data

def main():
    """
    Run program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] #Convert data to integers
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = last_5_sales()
    stock_data = calculate_stock(sales_columns)
    update_worksheet(stock_data, "stock")
    
main()