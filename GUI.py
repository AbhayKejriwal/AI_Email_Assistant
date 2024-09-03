import PySimpleGUI as sg
import pandas as pd
import os

def data_load(window, excel_file='__test__\\emails.xlsx'):
    # Check if the file exists
    if not os.path.isfile(excel_file):
        print(f"File not found: {excel_file}")
        return

    # Read data from the Excel file
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Check if required columns exist
    required_columns = {'From', 'Subject', 'Summary', 'Category'}
    if not required_columns.issubset(df.columns):
        print(f"Missing required columns in the Excel file.")
        return

    # Group data by category
    grouped_data = df.groupby('Category')

    # Update tables for each category
    categories = ['Important', 'NotImportant', 'Spam', 'CannotClassify']
    for category in categories:
        if category in grouped_data.groups:
            # Extract data for the current category
            category_data = grouped_data.get_group(category)
            # Prepare data for the table
            table_data = category_data[['From', 'Subject', 'Summary']].values.tolist()
            # Update the table in the GUI
            window[f'{category}_Table'].update(values=table_data)
        else:
            # If no data for this category, clear the table
            window[f'{category}_Table'].update(values=[])


# Assuming you have the window object from the GUI
# Call data_load to populate the tables
# data_load(window, excel_file_path)

def create_gui_layout(categories):
    tab_group = []
    
    # Define the layout for each tab
    for category in categories:
        layout = [
            [sg.Table(
                values=[], 
                headings=['From', 'Subject', 'Summary'], 
                max_col_width=50,
                auto_size_columns=False,     # Disable auto sizing
                display_row_numbers=False,
                justification='left',
                num_rows=10,
                key=f'{category}_Table',
                enable_events=True,
                background_color='white',     # Set the background color to white
                text_color='black',           # Set the text color to black
                font=('Helvetica', 10),       # Set the text font and size
                row_height=30,                # Increase row height to add space between rows
                col_widths=[25, 30, 45],      # Set column widths as percentages
                expand_x=True,  # Allow horizontal expansion
                expand_y=True   # Allow vertical expansion
            )]
        ]
        tab_group.append(sg.Tab(category, layout, key=category))

    layout = [
        [sg.TabGroup([tab_group], expand_x=True, expand_y=True)],  # Make the tab group resizable
        [sg.Button('Refresh', key='-REFRESH-'), sg.Exit()]
    ]
    
    return layout


def main():
    categories = ['Important', 'NotImportant', 'Spam', 'CannotClassify']
    file_path = "emails.xlsx"  # Path to your Excel file

    layout = create_gui_layout(categories)
    
    # Set the initial size of the window (width, height)
    window = sg.Window('Email Assistant', layout, resizable=True, size=(1000, 600), finalize=True)

    data_load(window, file_path)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-REFRESH-':
            data_load(window, file_path)

        for category in categories:
            if event == f'{category}_Table_Update':
                window[f'{category}_Table'].update(values[event])

    window.close()

if __name__ == "__main__":
    main()
