"""A web scraper for restaurant data using Selenium and BeautifulSoup.
Driver: Your Name
Navigator: None
Assignment: Final Project INST326
Date: Replace_with_submission_date

Challenges Encountered: This version uses mock HTML. Replace mock with Selenium logic when integrating with real websites.
"""

import sys
import argparse
import csv
from bs4 import BeautifulSoup

# Optional: Uncomment and use Selenium in actual implementation
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# This is a mock HTML string that simulates restaurant data you'd scrape from a website.
MOCK_HTML = """
<html>
  <body>
    <div class="restaurant">
      <h2 class="name">Saffron Garden</h2>
      <p class="cuisine">Indian, Vegetarian</p>
      <span class="rating">4.5</span>
    </div>
    <div class="restaurant">
      <h2 class="name">Green Leaf</h2>
      <p class="cuisine">Vegan, Organic</p>
      <span class="rating">4.7</span>
    </div>
    <div class="restaurant">
      <h2 class="name">Bistro Bella</h2>
      <p class="cuisine">French, Gluten-Free</p>
      <span class="rating">4.2</span>
    </div>
  </body>
</html>
"""

def main(dummy_url, output_file):
    # Simulate Selenium fetching page source from a real browser.
    # In real usage, you'd do something like:
    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    # driver.get(dummy_url)
    # html = driver.page_source
    # driver.quit()

    html = MOCK_HTML  # Placeholder for Selenium-generated HTML
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup parses the HTML

    data = []
    for restaurant in soup.find_all("div", class_="restaurant"):
        name = restaurant.find("h2", class_="name").text.strip()
        cuisine = restaurant.find("p", class_="cuisine").text.strip()
        rating = restaurant.find("span", class_="rating").text.strip()
        data.append({"name": name, "cuisine": cuisine, "rating": rating})

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "cuisine", "rating"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Scraped {len(data)} restaurants and saved to {output_file}")

def parse_args(args_list):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('required', type=str, help='Mock URL input (replace with real URL later)')
    parser.add_argument('--optional', '-o', type=str, default='restaurants.csv', help='Output CSV filename')
    return parser.parse_args(args_list)

if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:])
    main(arguments.required, arguments.optional)
