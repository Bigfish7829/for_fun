from datetime import datetime

import openpyxl
from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import pandas as pd
import os

process_time = {}
timestamp = {}
current_app = None
# Get the start time in hours, minutes, and seconds
start_time = datetime.now().strftime("%H_%M_%S")
day_of_the_week = datetime.now().strftime("%A")
week_number = datetime.now().strftime("%W")

# Excel file path
excel_file_path = f"C:\\Users\\JackPreece\\OneDrive - Sero\\Desktop\\process_time_{week_number}.xlsx"

# Check if the Excel file already exists
if os.path.exists(excel_file_path):
    # Load the existing data into a DataFrame
    existing_dict_of_dfs = pd.read_excel(excel_file_path, sheet_name=None)
    existing_dict_of_dfs = existing_dict_of_dfs[existing_dict_of_dfs['Application'] != 'Total']
else:
    # Create a new DataFrame if the Excel file doesn't exist
    existing_dict_of_dfs = pd.DataFrame(columns=['Application', 'TimeInSeconds'])
    existing_dict_of_dfs.to_excel(excel_file_path, index=False)
    new_wb = openpyxl.load_workbook(excel_file_path)
    new_wb.save(excel_file_path)

# Set the time threshold for saving data (every 5 minutes)
save_interval = 10
next_save_time = time.time() + save_interval
i=1
while True:
    try:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    except Exception as e:
        current_app = "Unknown"
    timestamp[current_app] = int(time.time())
    time.sleep(1)
    if current_app not in process_time.keys():
        process_time[current_app] = 0
    process_time[current_app] = process_time[current_app]+int(time.time())-timestamp[current_app]

    timestamp[current_app] = int(time.time())

    current_time = time.time()

    if current_time >= next_save_time:
        # Create a DataFrame from the process_time dictionary
        new_data = pd.DataFrame(process_time.items(), columns=['Application', 'TimeInSeconds'])


        if i == 1:
            # Add the existing data to the new data
            new_data = new_data.append(existing_dict_of_dfs, ignore_index=True)
        i += 1

        total_time = new_data['TimeInSeconds'].sum()
        # Calculate the total time in seconds and add it to the new data
        # Remove 'LockApp' from the total time (if it exists)
        if 'LockApp' in new_data['Application'].values:
            lock_app_time = new_data[new_data['Application'] == 'LockApp']['TimeInSeconds'].values
            total_time -= lock_app_time[0]
            new_data.loc[new_data['Application'] == 'Total', 'TimeInSeconds'] = total_time
        new_data = new_data.append({'Application': 'Total', 'TimeInSeconds': total_time}, ignore_index=True)

        new_data['TimeInMinutes'] = new_data['TimeInSeconds'] / 60
        new_data['TimeInHours'] = new_data['TimeInSeconds'] / 3600
        print(new_data)

        try:
            wb = openpyxl.load_workbook(excel_file_path)
            sheet_names = wb.get_sheet_names()


            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                new_data.to_excel(writer, sheet_name=day_of_the_week, index=False)
        except Exception as e:
            print(f"Error while saving Excel file: {e}. Waiting for the next save time.")

        next_save_time = current_time + save_interval
    #time.sleep(1)
