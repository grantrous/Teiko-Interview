def read_csv(file):
    import pandas as pd
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        return str(e)

def validate_data(data):
    if data.empty:
        return False, "The uploaded CSV file is empty."
    # Add more validation rules as needed
    return True, ""

def convert_to_dict(data):
    return data.to_dict(orient='records')