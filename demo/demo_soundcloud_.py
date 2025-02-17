# Merci chatGPT

from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    # Launch the browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Navigate to the target URL
    url = "https://soundcloud.com/search?q=JAAJ"
    page.goto(url)

    # Wait for the search results to load
    page.wait_for_selector('div.searchItem')

    # Extract the first result
    results = page.query_selector_all('div.searchItem')
    if results:
        first_result = results[0]

        # Extract title and artist
        title = first_result.query_selector('a.soundTitle__title').inner_text()
        artist = first_result.query_selector('a.soundTitle__username').inner_text()
        link = first_result.query_selector('a.soundTitle__title').get_attribute('href')

        # Extract the image URL from the span's style attribute
        span_element = first_result.query_selector('span.sc-artwork')
        if span_element:
            style = span_element.get_attribute('style')
            # Use regex to extract the URL from the style attribute
            match = re.search(r'url\("([^"]+)"\)', style)
            if match:
                image_url = match.group(1)
            else:
                image_url = "Image URL not found."
        else:
            image_url = "No artwork span found."

        # Print the extracted information
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print(f"Link: https://soundcloud.com{link}")
        print(f"Image URL: {image_url}")
    else:
        print("No results found.")

    # Close the browser
    browser.close()