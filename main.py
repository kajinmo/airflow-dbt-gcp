from utils.file_handlers import get_most_recent_filepath, read_data_file
from validator.validator import EngagementValidator

data_directory = 'include/data/'
file_extension = 'csv'
sep=','


try:
    # 1. Get the data filepath
    latest_file = get_most_recent_filepath(
        directory_path=data_directory,
        file_type=file_extension
    )
    print(f"Processing: {latest_file}")
    
    # 2. Read the file to DataFrame
    df = read_data_file(
        file_path=latest_file,
        file_type=file_extension,
        sep=sep
    )

    # 3. Validate
    validator = EngagementValidator(df)
    valid_data = validator.validate()
    print(f"Successfully validated {len(valid_data)} records")


except Exception as e:
    print(f"Processing failed: {str(e)}")
    raise

print(valid_data)