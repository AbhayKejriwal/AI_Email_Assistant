import pandas as pd
from datetime import datetime
import openpyxl

def read_from_excel(file_name):
    # Read Excel file into DataFrame
    df = pd.read_excel(file_name)
    
    # Convert DataFrame to list of dictionaries
    dict_list = df.to_dict(orient="records")
    
    return dict_list

def save_to_excel(dict_list, file_name=None):
    # If file name is not provided, set it to current date and time
    if file_name is None:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"data_{current_time}.xlsx"
    
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(dict_list)
    # Write DataFrame to Excel file
    df.to_excel(file_name, index=False)

# Example usage
if __name__ == "__main__":
    # Example list of dictionaries
    data = [
        {"Name": "John", "Age": 30, "City": "New York"},
        {"Name": "Alice", "Age": 25, "City": "Los Angeles"},
        {"Name": "Bob", "Age": 35, "City": "Chicago"}
    ]
    
    # Convert and save to Excel with default file name
    save_to_excel(data, "output.xlsx")
    print("Data written.")

    # Input file name
    input_file = "output.xlsx"
    
    # Convert Excel to list of dictionaries
    data = read_from_excel(input_file)
    print("Data read from Excel file:")
    print(data)
