
import os
import requests
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures



def get_hrefs(url):

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Locate the div with class "filter-results"
        filter_results_div = soup.find("div", class_="filter-results")

        # Check if the div is found
        if filter_results_div:
            hrefs=[]
            # Iterate through the div elements with class "filter-result"
            for result_div in filter_results_div.find_all("div", class_="filter-result"):
                # Find the anchor (a) element within the div
                a_tag = result_div.find("a", class_="filter-result__name", href=True)

                # Check if the anchor element is found
                if a_tag:
                    # Get the href attribute
                    href = a_tag["href"]
                    hrefs.append(href)

                    # Print or inspect the href
                    # print("Found href:", href)

            return hrefs

        else:
            print("Could not find div with class 'filter-results'")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def get_instelling_info(url):
    response = requests.get(url)

    default = {
                "company": None,
                "marked_segment": None,
                "address": None,
                "phone_number": None,
                "website": None,
                "url": url
                }

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        try:
            soup = BeautifulSoup(response.content, "html.parser")
        except:
            print("failed to parse html content")
            return default

        # Extract information from the modal content
        try:
            title_element = soup.find("div", class_="mb-1").find("h1")
            company = title_element.text.strip() if title_element else None
        except:
            company = None

        # markt segtment
        try:
            subtitle_element = soup.find("p", class_="mb-2")
            marked_segment = subtitle_element.text.strip() if subtitle_element else None
        except:
            marked_segment = None


        try:
            address_button = soup.find("button", class_="modal-address-toggle")
            if address_button:
                # address = address_button.text.strip()[1:]  # Remove the initial icon
                address = address_button.text.strip()  # Remove the initial icon
        except:
            address = None
        
        try:
            phone_number_element = phone_number = soup.find("a", class_="underline")
            phone_number = phone_number_element.text.strip()
        except:
            phone_number = None

        # Check if the website element is found before trying to access its href attribute
        try:
            website_element = soup.find("a", class_="underline", target="_blank")
            website = website_element["href"] if website_element else None
        except:
            website = None

        return {
            "company": company,
            "marked_segment": marked_segment,
            "address": address,
            "phone_number": phone_number,
            "website": website,
            "source_url": url,
            }
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return default

def write_to_csv(info_list, csv_file, fieldnames):

    # Check if the file already exists
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is newly created
        if not file_exists:
            writer.writeheader()

        for info in info_list:
            writer.writerow(info)


def main():
    base_url = "https://www.zorgkaartnederland.nl"
    url = "https://www.zorgkaartnederland.nl/zorginstelling"
    route = "/pagina"

    urls = [url] + [url + route + str(i) for i in range(3010) if i > 1]  
    # urls = [url + route + str(i) for i in range(3010) if i > 424]  

    for url in urls:
        print(url)

        try:
            hrefs = get_hrefs(url)
        except:
            continue

        target_urls = [base_url + href for href in hrefs]

        info_list = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(get_instelling_info, target_url): target_url for target_url in target_urls}
            for future in concurrent.futures.as_completed(futures):
                target_url = futures[future]
                try:
                    info = future.result()
                    info_list.append(info)
                except Exception as exc:
                    print(f"Failed to get info for {target_url}. Error: {exc}")

        
        csv_file = "output.csv"
        fieldnames = list(info_list[0].keys()) # fieldnames = ["company", "marked_segment", "address", "phone_number", "website", "source_url"]
        write_to_csv(info_list, csv_file, fieldnames)
            
        



if __name__=="__main__":
    main()