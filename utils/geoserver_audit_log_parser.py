#!/usr/bin/python3

import csv
import argparse
import os
import glob
from datetime import datetime, timedelta

# Define the width for each field/column
column_widths = {
    'id': 25, 
    'internalHost': 25, 
    'service': 25,  
    'owsVersion': 25, 
    'operation': 25, 
    'subOperation': 25, 
    'layer': 25, 
    'bbox': 80, 
    'path': 25,
    'queryString': 400,
    'bodyAsString': 25,
    'httpMethod': 25, 
    'startTime': 35, 
    'endTime': 35, 
    'totalTime': 25, 
    'remoteAddr': 25, 
    'remoteUser': 25, 
    'remoteUserAgent': 25, 
    'responseStatus': 25, 
    'responseLength': 25, 
    'responseContentType': 25, 
    'error': 25, 
    'errorMessage': 50
}

all_fields = ['id', 
                  'internalHost', 
                  'service',  
                  'owsVersion', 
                  'operation', 
                  'subOperation', 
                  'layer', 
                  'bbox', 
                  'path',
                  'queryString',
                  'bodyAsString',
                  'httpMethod', 
                  'startTime', 
                  'endTime', 
                  'totalTime', 
                  'remoteAddr', 
                  'remoteUser', 
                  'remoteUserAgent', 
                  'responseStatus', 
                  'responseLength', 
                  'responseContentType', 
                  'error', 
                  'errorMessage']

# Parse CSV log file
def parse_log_file(audit_files, errors_only=False, ip=None, limit=None, start_position=0):
    
    # Limit counter
    lines_printed = 0
    limit_exit = False

    for file_path in audit_files:
        if limit_exit:
            break
        print(f"Parsing file: {file_path}")
        
        # Open the file manually
        file = open(file_path, mode='r')

        try:
            csv_reader = csv.DictReader(file, fieldnames=all_fields)
            
            for row in reversed(list(csv_reader)):
                remoteAddr = row.get('remoteAddr', '')
                state = row.get('error', '').lower() if row.get('error') else ''
                level = 'error' if state == 'true' else 'info'

                # Build the formatted output with custom column widths
                formatted_output = f"{level:<7}"
                for field in fields_to_parse:
                    value = row.get(field, "")
                    width = column_widths.get(field, 25)  # Default to 20 if no custom width is specified
                    formatted_output += f"{value:<{width}}"

                # Filter by errors if the --errors-only flag is set
                if errors_only and level != 'error':
                    continue
                
                # Filter by IP if the --ip flag is set
                if ip and ip != remoteAddr:
                    continue
                
                print(formatted_output, end="\n", flush=True)
                
                lines_printed += 1
                if limit and lines_printed >= limit:
                    limit_exit = True
                    break
        finally:
            file.close()  # Ensure the file is closed properly

def get_audit_files(directory, time_limit=None):

    log_files = glob.glob(os.path.join(directory, '*.log'))
    log_files.sort(reverse=True)
    
    audit_files = []
    now = datetime.now()
    
    for file_path in log_files:
        file_outside_limit = True
        if time_limit:
            # Get the file's last modification time
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            # Check if the file is within the time limit
            if now - mod_time <= time_limit:
                file_outside_limit = False
                audit_files.append(file_path)
            if file_outside_limit:
                return audit_files
        else:
            audit_files.append(file_path)
    return audit_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and highlight errors/warnings in a CSV log file.")
    parser.add_argument('-e', '--errors-only', action='store_true', help="Only display errors from the log file")
    parser.add_argument('-s', '--since', help="Filter files modified within this time period (e.g., '15m' for 15 minutes)", type=str)
    parser.add_argument('-d', '--directory', help="Path to the directory containing log files")
    parser.add_argument('-f', '--fields', help="""Comma-separated list of additional fields to include in the output \n
                                            Supported fields:
                                            'id', 
                                            'internalHost', 
                                            'service',  
                                            'owsVersion', 
                                            'operation', 
                                            'subOperation', 
                                            'layer', 
                                            'bbox', 
                                            'path',
                                            'queryString',
                                            'bodyAsString',
                                            'httpMethod', 
                                            'startTime', 
                                            'endTime', 
                                            'totalTime', 
                                            'remoteAddr', 
                                            'remoteUser', 
                                            'remoteUserAgent', 
                                            'responseStatus', 
                                            'responseLength', 
                                            'responseContentType', 
                                            'error', 
                                            'errorMessage'
                                        """)
    parser.add_argument('-t', '--tail', action='store_true', help="Continuously monitor the directory for new log files and process them")
    parser.add_argument('--ip', help="Filter log entries by IP address", type=str)
    parser.add_argument('-l', '--limit', help="Limit the number of log lines to print", type=int, required=False)
    
    
    args = parser.parse_args()

    #  Parse the fields argument as a comma-separated string
    fields = args.fields.split(",") if args.fields else None

    # Parse the directory argument
    directories = args.directory.split(",") if args.directory else './'

    # Parse the --since argument
    time_period = args.since
    time_limit = None
    if time_period:
        if time_period.endswith('m'):
            minutes = int(time_period[:-1])
            time_limit = timedelta(minutes=minutes)
        elif time_period.endswith('h'):
            hours = int(time_period[:-1])
            time_limit = timedelta(hours=hours)
        elif time_period.endswith('d'):
            days = int(time_period[:-1])
            time_limit = timedelta(days=days)
        else:
            raise ValueError("Unsupported time period format. Use 'm' for minutes or 'h' for hours.")

    # Print header dynamically based on fields
    header = f"{'Level':<7}"
    default_fields = ['startTime', 'remoteAddr', 'operation', 'errorMessage']
    fields_to_parse = default_fields if fields is None else default_fields + fields 
    for field in fields_to_parse:
        width = column_widths.get(field, 25) 
        header += (f"{field.capitalize():<{width}}")
    print(header)
    print('-' * len(header))

    # Get the audit log files
    for directory in directories:
        audit_files = get_audit_files(directory, time_limit)
        if audit_files:
            parse_log_file(audit_files, errors_only=args.errors_only, ip=args.ip, limit=args.limit)
        else:
            print("No log files found.")
