import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = 'output.csv'
df = pd.read_csv(file_path)


# def remove_website_from_phone_nr(df):
#     # Create a mask to identify rows where 'phone_number' looks like a website
#     website_mask = df['phone_number'].str.contains(r'http[s]?://', case=False, na=False)

#     # Move values from 'phone_number' to 'website' for rows where the mask is True
    # df.loc[website_mask, ['phone_number', 'website']] = np.nan, df.loc[website_mask, 'phone_number']
    
def remove_website_from_phone_nr(df):
    # Create a mask to identify rows where 'phone_number' looks like a website
    website_mask = df['phone_number'].str.contains(r'http[s]?://', case=False, na=False)

    # Move values from 'phone_number' to 'website' for rows where the mask is True
    df.loc[website_mask, 'website'] = df.loc[website_mask, 'phone_number']
    df.loc[website_mask, 'phone_number'] = np.nan


def clean_phone_number(df):
    df['phone_number'] = df['phone_number'].replace('[^0-9]', '', regex=True)
    
def is_main_location_in_company(row):
    if 'locatie' in row['company']:
        return False
    else:
        return True

def add_is_main_location_column(df, fn):
    # Apply the function to create a new column 'branch_type'
    df['is_main_location'] = df.apply(fn, axis=1)

    


remove_website_from_phone_nr(df)
clean_phone_number(df)
add_is_main_location_column(df, is_main_location_in_company)

df.to_csv("output_cleaned.csv", index=False)
# print(df.head())

# row_172_info = df.loc[172, ['website', 'phone_number']]
# print(row_172_info)


