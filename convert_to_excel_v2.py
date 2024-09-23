import pandas as pd
import re
#{"x": 0.0, "y": 0.0, "z": -0.03, "roll": 0.0, "pitch": 0.0, "yaw": 0.0, "button0": 0, "button1": 0, "timeStamp": "2024-09-20 09:51:21.793"}
def parse_log_line(line):
    # Regular expression to extract timestamp, category, and message
    match = re.match(r'(\d{4}-\d{2}-\d{2}) - (\d{2}:\d{2}:\d{2}\.\d{3}) - (\w+) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) - (,*)', line)
    
    if match:
        date, time, Event, originalTimeStamp,message = match.groups()
        return Event,originalTimeStamp
    return None, None
def parse_log_line_2(line):
    # Regular expression to extract timestamp, category, and message
    match = re.match(r'(\d{4}-\d{2}-\d{2}) - (\d{2}:\d{2}:\d{2}\.\d{3}) - (\w+) - (.*)', line)

    if match:
        date,timestamp, Event, message = match.groups()
        return Event,timestamp
    return None, None
def log_to_dataframe(log_file_path):
    beforeWebsocket=None
    robotExecution=None
    data = {'BeforeWebsocket': [], 'robotExecution': []}
    
    with open(log_file_path, 'r') as file:
        checkEvent="BeforeWebsocket"
        Event=None
  
        for line in file:
            match1 = re.search(r'..*BeforeWebsocket.*}', line)
            match2 = re.search(r'.*RobotExecution .*]', line)

            
            if match1:              
               Event,timestamp = parse_log_line(line.strip())
               beforeWebsocket=timestamp
                         
            if match2:
                Event,timestamp2 = parse_log_line_2(line.strip())
                robotExecution=timestamp2
                print(Event)
       
            
            if match1 or match2:
               if Event== "RobotExecution": 

                if checkEvent != Event:
                   
                   data['BeforeWebsocket'].append(beforeWebsocket)
                   data['robotExecution'].append(robotExecution)
                
            checkEvent=Event                   
    
    return pd.DataFrame(data)

def save_to_excel(dataframe, excel_file_path):
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Logs')

# Path to the input text file and output Excel file
log_file_path = 'C:\\Users\\siva1\\Desktop\\Github\\text2excel\\test_tril_1.txt'  # Change this to your log file path
excel_file_path = 'c:\\Users\\siva1\\Desktop\\Github\\text2excel\\test_trail_1.xlsx'  # Change this to your desired output file path

# Convert log file to DataFrame and save to Excel
df = log_to_dataframe(log_file_path)
save_to_excel(df, excel_file_path)

print(f"Data has been successfully written to {excel_file_path}")