import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

booklist = []

# Changed: Modified get_response to accept a single url parameter instead of base_url and page_num
def get_response(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Request successful. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit()
    
    return response

def get_info(response):
    soup = BeautifulSoup(response.content, 'lxml')

    products = soup.find_all('article', class_='product_pod')

    for product in products:
        title = product.h3.a['title'] if product.h3 and product.h3.a else 'N/A'
        price = product.find('p', class_='price_color').text.strip() if product.find('p', class_='price_color') else 'N/A'
        rating = product.find('p', class_='star-rating')['class'][1] if product.find('p', class_='star-rating') else 'N/A'

        booklist.append({'title': title, 'price': price, 'rating': rating})
    
    next = soup.find('li', class_='next')

    if next != None:
        return True
    else:
        return False

# Changed: Modified main to use dynamic pagination with a while loop, handle first page URL, and remove the for loop
def main():
    page_num = 1  # Added: Initialize page number
    while True:  # Added: Use an infinite loop to continue until no next page
        # Added: Conditional URL for the first page vs. subsequent pages
        url = "https://books.toscrape.com/index.html" if page_num == 1 else "https://books.toscrape.com/catalogue/page-{}.html".format(page_num)
        resp = get_response(url)  # Changed: Pass the full url to get_response
        has_next = get_info(resp)  # Added: Store the boolean return value
        if not has_next:  # Added: Break the loop if there’s no next page
            break
        page_num += 1  # Added: Increment page number for the next iteration
        # time.sleep(3)
    
    df = pd.DataFrame(booklist)
    df.to_csv('raw_data.csv', index=False)



if __name__ == "__main__":
    main()