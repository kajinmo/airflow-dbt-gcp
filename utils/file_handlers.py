from datetime import datetime, timedelta
from typing import Optional
import os
import pandas as pd



def get_most_recent_filepath(directory_path: str,
                                     file_type: str,
                                     pattern: Optional[str] = None) -> str:
    """
    Returns the most recent filepath in a directory based on file extension and optional filename pattern.
    """
    # Get a list of all files in the directory
    if pattern:
        files = [f for f in os.listdir(directory_path) if (f.endswith(file_type) and pattern.lower() in f.lower())]
    else:
        files = [f for f in os.listdir(directory_path) if f.endswith(file_type)]
    if not files:
        raise FileNotFoundError(f"No files with extension {file_type} found in {directory_path}.")
        
    # Initialize an empty dictionary to store modification times
    modif_time = {}

    # Checks the latest file of designed file type in directory
    for file in files:
        file_path = os.path.join(directory_path, file)
        modif_time[file_path] = os.path.getmtime(file_path)

    # Get latest filepath
    return max(modif_time, key=modif_time.get)



def read_data_file(file_path: str, 
                  file_type: str, 
                  index_col: bool = False, 
                  **kwargs) -> pd.DataFrame:
    """
    Reads a data file (CSV/Excel) into a DataFrame.
    """
    file_type = file_type.lower()

    if file_type in ('xls', 'xlsx', '.xls', '.xlsx'):
        return pd.read_excel(
            file_path, 
            index_col=index_col, 
            engine='openpyxl', 
            **kwargs
        )
        
    elif file_type in ('xlsb', '.xlsb'):
        return pd.read_excel(
            file_path, 
            engine='pyxlsb', 
            index_col=index_col, 
            **kwargs
        )
        
    elif file_type in ('csv', 'csv.gz', '.csv', '.csv.gz'):
        return pd.read_csv(
            file_path, 
            index_col=index_col, 
            **kwargs
        )
        
    else:
        raise ValueError(f"Unsupported file type: {file_type}")