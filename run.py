import gspread
from google.oauth2.service_account import Credentials

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
        
def update_sales_worksheet(data):
    """
    Updates sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")  #gives feedback of whats happening
    sales_worksheet = SHEET.worksheet("sales") #value is name of sheet in the file
    sales_worksheet.append_row(data) #appends our input data to the sheet
    print("Sales Worksheet updated! \n") #confirms sheet is updated

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)

print("Welcome to Love Sandwiches Data Automation.")
main()