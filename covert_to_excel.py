import pandas as pd
import re

def parse_log_line(line):
    # Regular expression to extract timestamp, category, and message
    match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) - (\w+) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', line)
    print(match)
    if match:
        timestamp, Event, originalTimeStamp = match.groups()
        return originalTimeStamp, Event
    return None, None
def parse_log_line_2(line):
    # Regular expression to extract timestamp, category, and message
    match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) - (\w+) - (.*)', line)
    
    if match:
        timestamp, Event, message = match.groups()
        return timestamp, Event
    return None, None
def log_to_dataframe(log_file_path):
    data = {'Timestamp': [], 'Event': []}
    
    with open(log_file_path, 'r') as file:
        for line in file:
            match1 = re.search(r'.*BeforeWebsocket.*}', line)
            match2 = re.search(r'.*robotExecution .*]', line)
        
            if match1 :
             timestamp, category = parse_log_line(line.strip())
             if timestamp:
                data['Timestamp'].append(timestamp)
                data['Event'].append(category)
            if match2 :
             timestamp2, category2 = parse_log_line_2(line.strip())
             if timestamp2:
                data['Timestamp'].append(timestamp2)
                data['Event'].append(category2)
                              
    
    return pd.DataFrame(data)

def save_to_excel(dataframe, excel_file_path):
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Logs')

# Path to the input text file and output Excel file
log_file_path = 'C:\\Users\\siva1\\Desktop\\Github\\text2excel\\collectedData.txt'  # Change this to your log file path
excel_file_path = 'c:\\Users\\siva1\\Desktop\\Github\\text2excel\\collected_data2.xlsx'  # Change this to your desired output file path

# Convert log file to DataFrame and save to Excel
df = log_to_dataframe(log_file_path)
save_to_excel(df, excel_file_path)

print(f"Data has been successfully written to {excel_file_path}")