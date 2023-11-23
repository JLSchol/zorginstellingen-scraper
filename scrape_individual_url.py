import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Optional
import re



  


def get_page_links(soup: BeautifulSoup, domain: str) -> Optional[list[str]]:
    if soup:
        links = []
        for link in soup.find_all('a'):
            url = link.get('href')
            if domain in str(url) and url.startswith("http"):
                links.append(link.get('href'))

        return link

def find_number_via_regex(soup: BeautifulSoup, expression) -> Optional[str]:
        # Find all text in the soup
    all_text = soup.get_text()

    # Define a regular expression pattern for matching phone numbers
    phone_number_pattern = re.compile(expression)

    # Search for the pattern in the text
    match = phone_number_pattern.search(all_text)

    if match:
        phone_number = match.group(0)
        return phone_number
    else:
        return None

def find_numbers_via_tel_tag(soup: BeautifulSoup, expression: str) -> Optional[list[str]]:
    # Find all <a> tags with href starting with 'tel:'
    tel_links = soup.find_all('a', href=re.compile(r'^tel:'))

    # Extract phone numbers from the href attributes
    phone_numbers = [re.search(r'\d+', link['href']).group() for link in tel_links]
    numbers_filtered = [number for number in phone_numbers if len(number) > 6]

    if len(numbers_filtered) == 0:
        return None

    return numbers_filtered

def find_number(soup: BeautifulSoup) -> Optional[str]:
    print('finding number')
    numbers = None

    pattern_chad2 = r'\b(?:\+\d{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0[1-9][0-9]?[ -]?)?([0-9]{9}$|[0-9\-\s]{10}$|^0[0-9]{2}-[0-9]{7,8}$)\b'
    
    numbers = find_numbers_via_tel_tag(soup, pattern_chad2)

    if numbers is None:
        number = find_number_via_regex(soup, pattern_chad2)
        if number is not None:
            numbers = [number]

    if numbers is None:
        print("Phone number not found on the page.")
    else:
        print(numbers)

    return numbers

def find_email(soup: BeautifulSoup):
    print('finding email')

def find_address(soup: BeautifulSoup, row: pd.Series):
    print('find adres based on (gelocation), or soup')
    
def get_url(src: str) -> str:
    return src if src.startswith("http") else "http://" + src

def get_soup(url: str) -> Optional[BeautifulSoup]:
    # define general header to avoid 403 errors
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"could not get soup for {url=} becouse of {response.status_code=}")
  
def update_df_with_results(df: pd.DataFrame, results: list[dict]) -> pd.DataFrame:
    return df

def run(index: int, row: pd.Series) -> dict:
    result = {  'e-mail': None,
                'phone_number': None,
                'address': None
                }
    
    # check if has a website
    if pd.isna(row['website']):
        return result
    
    url = get_url(row['website'])
    soup = get_soup(url)


    if pd.isna(row['phone_number']):
        result['phone_number'] = find_number(soup)

    # find_email(soup)

    # find_address(soup, row)

    return result
      

def main():

    file_name = "test_url_scrape"
    output_id = ""

    file_in = file_name + ".csv"
    file_out = file_name + output_id +'_enhanced.csv'
    
    # read file as df
    df = pd.read_csv(file_in)

    # loop over the rows
    results = []
    for index, row in df.iterrows():
        print(row['company'])
        results.append(run(index, row))


    # update df
    df = update_df_with_results(df, results)

    # write df out as csv
    df.to_csv(file_out, index=False)



if __name__ == "__main__":
    main()
