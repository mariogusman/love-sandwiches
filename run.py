import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures input from the user
    Loops through the input requests while the result from validate_date is false
    Once data is valid we confirm that to the user and break the script
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60")
        
        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data
    
def validate_data(values):
    """
    Inside the try, converts all strings values into ints.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"We need 6 values but you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}. \nPlease try again.\n")
        return False
    
    return True
        

    
def update_worksheet(data,worksheet):
    """
    Received list of ints to be inserted into a worksheet
    Update relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated!")
    
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calc the suplus for each item type.
    Surplis is defined as the sales figures subtracted from the stock
    - positive surplus = waste
    - negative surplis = extra sandwiches had to be made
    """
    print("... calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
    return surplus_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")

print("Welcome to Love Sandwiches Data Automation.")
main()