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
    
def is_main_location_based_on_company_name(row):
    if 'Woonlocatie ' in row['company']:
        return False
    elif 'locatie ' in row['company']:
        return False
    else:
        return True
    
# def is_main_location_based_on_marked_segment_and_number(df, row):
#     if row['marked_segment'] == 'Organisatie':
#         match_partial_str_count(df, )
#         # check if name

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
        print("processing row " + str(index))

        if row['is_main_location']:
            if not pd.isnull(row['website']):
                counts = match_field_count(df, index, row, 'website', counts)
            elif not pd.isnull(row['company']):
                counts = match_partial_str_count(df, index, row, 'company', counts)
            elif not pd.isnull(row['phone_number']):
                counts = match_field_count(df, index, row, 'phone_number', counts)
            else:
                counts[index] == 1
                print("no match for {} on company name, phone number and website".format(row['company']))       
                          
            # # if there is more than one location and "Organisatie" as marked segment, update with correct segment
            # if (counts[index] > 1) and (str(row['marked_segment']) == 'Organisatie'):
            #     # update marked segment in hooflocatie (based on phone number match..)
            #     update_marked_segment_main_location(df, index, row)

    # Convert the dictionary to a Series and assign it to the DataFrame
    df['nr_of_locations'] = pd.Series(counts)
    
def drop_non_main_locations(df):
    # Drop rows where is_main_location is False
    df = df[df['is_main_location']].copy()
    df.drop('is_main_location', axis=1, inplace=True)
    return df

def clean_website(df):
    # Ensure the 'website' column is of type string
    df['website'] = df['website'].astype(str)

    # Remove 'http://' or 'https://'
    df['website'] = df['website'].str.replace(r'^https?://', '', regex=True)

    # Remove 'www.'
    df['website'] = df['website'].str.replace(r'^www\.', '', regex=True)

    # Extract the root domain
    df['website'] = df['website'].str.extract(r'([a-zA-Z0-9-]+\.[a-zA-Z]+)', expand=False)

    return df

def update_main_location(df):
    filtered_rows = df[(df['marked_segment'] == 'Organisatie') & (df['nr_of_locations'] > 1)]
    associated_locations = None
    for _, row in filtered_rows.iterrows():
        if not pd.isnull(row['website']):
            associated_locations = df[df['website'] == row['website']]
        
        elif not pd.isnull(row['phone_number']):
            associated_locations = df[df['phone_number'] == row['phone_number']]

        else:
            return
        
        if associated_locations is not None:
            for _, associated_row in associated_locations.iterrows():
                if associated_row['marked_segment'] == 'Organisatie':
                    df.at[associated_row.name, 'is_main_location'] = True
                else:
                    df.at[associated_row.name, 'is_main_location'] = False

def keep_unique_field_with_shortest_company_name(df, field):
        # DataFrame with non-NaN and non-empty 'website' values
    df_without_nan = df[df[field].notna() & (df[field] != '')]

    # DataFrame with NaN or empty field values
    df_with_nan = df[df[field].isna() | (df[field] == '')]
    
    df_sorted = df_without_nan.sort_values(by='company', key=lambda x: x.str.len())
    df_unique = df_sorted.drop_duplicates(subset=field, keep='first')

    df_result = pd.concat([df_unique, df_with_nan])
    
    return df_result



def main():
    # file_name = 'output'
    # output_id = "_website_count"
    file_name = 'test_output'
    output_id = ""

    file_in = file_name + ".csv"
    file_out = file_name + output_id +'_processed.csv'
    
    df = pd.read_csv(file_in)
    
    remove_website_from_phone_nr(df)
    
    clean_phone_number(df)

    df = clean_website(df)
    
    add_is_main_location_column(df, is_main_location_based_on_company_name)
    
    add_locations_column_and_update_marked_segment(df)
    
    update_main_location(df)

    df = drop_non_main_locations(df) # these are safe to drop

    # these work not properly! (before we drop them, we should have updated the nr_of_locations!)
    # df = keep_unique_field_with_shortest_company_name(df, 'website')

    # df = keep_unique_field_with_shortest_company_name(df, 'phone_number')
    
    df.to_csv(file_out, index=False)
    
    # print(df.loc[:, ['company','marked_segment', 'phone_number', 'nr_of_locations']])


if __name__ == "__main__":
    main()









