import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame


    
def remove_website_from_phone_nr(df):
    # Create a mask to identify rows where 'phone_number' looks like a website
    website_mask = df['phone_number'].str.contains(r'http[s]?://', case=False, na=False)

    # Move values from 'phone_number' to 'website' for rows where the mask is True
    df.loc[website_mask, 'website'] = df.loc[website_mask, 'phone_number']
    df.loc[website_mask, 'phone_number'] = np.nan

def clean_phone_number(df):
    df['phone_number'] = df['phone_number'].replace('[^0-9]', '', regex=True)
    
def is_main_location_in_company(row):
    if 'Woonlocatie ' in row['company']:
        return False
    elif 'locatie ' in row['company']:
        return False
    else:
        return True

def add_is_main_location_column(df, fn):
    # Apply the function to create a new column 'branch_type'
    df['is_main_location'] = df.apply(fn, axis=1)

def phone_number_match_count(df: pd.DataFrame, index: int, row: pd.Series, counts: dict) -> dict:
    # If it's a main location, count the number ofphphone_number_match_count associated locations with the same phone number
    phone_number = row['phone_number']
    associated_locations = df[df['phone_number'] == phone_number]
    nr_of_locations = len(associated_locations)  # include the main location itself
    counts[index] = nr_of_locations
    return counts

def match_field_count(df: pd.DataFrame, index: int, row: pd.Series, field: str, counts: dict) -> dict:
    # If it's a main location, count the number ofphphone_number_match_count associated locations with the same phone number
    check = row[field]
    matches = df[df[field] == check]
    nr_of_matches = len(matches)  # include the main location itself
    counts[index] = nr_of_matches
    return counts
    
def match_partial_str_count(df: pd.DataFrame, index: int, row: pd.Series, field: str, counts: dict) -> dict:
    # If it's a main location, count the number ofphphone_number_match_count associated locations with the same phone number
    to_be_matched = row[field]
    matches = df['company'].str.contains(to_be_matched, case=False, na=False)
    nr_of_matches = matches.sum() # count nr of true values ()
    counts[index] = nr_of_matches
    return counts

def update_marked_segment_main_location(df: pd.DataFrame, index: int, row: pd.Series):
        main_location_name = row['company']
        associated_locations = None
        if not pd.isnull(row['phone_number']):
            associated_locations = df[df['phone_number'] == row['phone_number']]
        # try match on phone nr
        elif not pd.isnull(row['website']):
            associated_locations = df[df['website'] == row['website']]
        
        if associated_locations is None:
            "could not find associated location to update 'Organisatie"
            return 
        
        # Exclude the main location itself
        associated_locations = associated_locations[associated_locations['company'] != main_location_name]
        
        if not associated_locations.empty:
            # Use the marked_segment from the first associated location
            new_marked_segment = associated_locations.iloc[0]['marked_segment']
            df.at[index, 'marked_segment'] = new_marked_segment

def add_locations_column_and_update_marked_segment(df):
    # Create a dictionary to store the count of associated locations based on phone number
    counts = {}

    # Iterate through the DataFrame
    for index, row in df.iterrows():

        if row['is_main_location']:
            if not pd.isnull(row['company']):
                counts = match_partial_str_count(df, index, row, 'company', counts)
            elif not pd.isnull(row['phone_number']):
                counts = match_field_count(df, index, row, 'phone_number', counts)
            elif not pd.isnull(row['website']):
                counts = match_field_count(df, index, row, 'website', counts)
            else:
                print("no match for {} on company name, phone number and website".format())       
                          
            # if there is more than one location and "Organisatie" as marked segment, update with correct segment
            if (counts[index] > 1) and (str(row['marked_segment']) == 'Organisatie'):
                # update marked segment in hooflocatie (based on phone number match..)
                update_marked_segment_main_location(df, index, row)

    # Convert the dictionary to a Series and assign it to the DataFrame
    df['nr_of_locations'] = pd.Series(counts)
    
def drop_non_main_locations(df):
    # Drop rows where is_main_location is False
    df = df[df['is_main_location']]
    df.drop('is_main_location', axis=1, inplace=True)
    return df

    
def main():
    file_in = 'output.csv'
    file_out = 'output_processed.csv'
    
    df = pd.read_csv(file_in)
    
    remove_website_from_phone_nr(df)
    
    clean_phone_number(df)
    
    add_is_main_location_column(df, is_main_location_in_company)
    
    add_locations_column_and_update_marked_segment(df)
    
    df = drop_non_main_locations(df)
    
    df.to_csv(file_out, index=False)
    
    # print(df.loc[:, ['company','marked_segment', 'phone_number', 'nr_of_locations']])


if __name__ == "__main__":
    main()









