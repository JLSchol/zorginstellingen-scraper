import pandas as pd
import numpy as np

def remove_website_from_phone_nr(df):
    # Create a mask to identify rows where 'phone_number' looks like a website
    website_mask = df['phone_number'].str.contains(r'http[s]?://', case=False, na=False)

    # Move values from 'phone_number' to 'website' for rows where the mask is True
    df.loc[website_mask, 'website'] = df.loc[website_mask, 'phone_number']
    df.loc[website_mask, 'phone_number'] = np.nan

def clean_phone_number(df):
    df['phone_number'] = df['phone_number'].replace('[^0-9]', '', regex=True)
    
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

def count_locations(df):
    # Conditionally count based on 'website' or 'phone_number'
    df['nr_of_locations'] = df.apply(lambda row: row['phone_number'] if pd.isnull(row['website']) else row['website'], axis=1)
    df['nr_of_locations'] = df.groupby('nr_of_locations')['nr_of_locations'].transform('count').fillna(0)

def drop_duplicates_based_on_unique(df, field):
    # split df into nan and no nan values ()
    df_without_nan = df[df[field].notna() & (df[field] != '')]
    df_with_nan = df[df[field].isna() | (df[field] == '')]

    # sorted based on length of company name
    df_sorted = df_without_nan.sort_values(by='company', key=lambda x: x.str.len())

    # drop duplicates and keep the First (shortest name)
    df_unique = df_sorted.drop_duplicates(subset=field, keep='first')

    # append the nan values back since we do not want to drop them
    df_result = pd.concat([df_unique, df_with_nan])
    
    return df_result

def prepend_www_to_website(df):
    df['website'] = df['website'].apply(lambda x: f'www.{x}' if pd.notnull(x) else x)



def main():

    file_name = 'output'
    output_id = ""

    file_in = file_name + ".csv"
    file_out = file_name + output_id +'_p2.csv'
    
    df = pd.read_csv(file_in)


    remove_website_from_phone_nr(df)
    clean_phone_number(df)
    clean_website(df)

    count_locations(df)

    df = drop_duplicates_based_on_unique(df, 'website')

    prepend_www_to_website(df)

    print(df.head())


    df.to_csv(file_out, index=False)



if __name__ == "__main__":
    main()


