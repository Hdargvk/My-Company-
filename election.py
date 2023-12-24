import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def scrape_table_data(table):
    data_to_write = []
    for row in table.find_elements(By.XPATH, ".//tr"):
        row_data = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
        if row_data:
            data_to_write.append(row_data)
    return data_to_write


# Specify the path to the geckodriver executable
geckodriver_path = r"C:\Users\Dell\Downloads\geckodriver-v0.33.0-win32\geckodriver.exe"

# Specify the path to the Firefox binary
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# Set up Firefox WebDriver using the specified executable path and binary path
firefox_options = FirefoxOptions()
firefox_options.binary_location = firefox_binary_path
firefox_service = FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

# URLs of the websites to scrape
urls = [
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS121.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS122.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS123.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS124.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS125.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS126.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS127.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS128.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS129.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS1210.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS1211.htm",
    "https://results.eci.gov.in/AcResultGenDecNew2023/statewiseS1212.htm",
]

temp_dir = tempfile.gettempdir()
csv_filename = os.path.join(temp_dir, "website_data.csv")

for url in urls:
    driver.get(url)

    # Use WebDriverWait to wait for the visibility of any table on the page
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            # This will wait for the presence of any table on the page
            table = wait.until(EC.visibility_of_element_located((By.XPATH, "//table")))
        except Exception as e:
            # No table found, break out of the loop
            break

        # Extract data from the current page
        data_to_write = scrape_table_data(table)

        # Create and write data to a CSV file
        with open(csv_filename, "a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the data
            csv_writer.writerows(data_to_write)

        # Find the element that allows you to move to the next page (e.g., a "Next" button)
        try:
            next_page_button = driver.find_element(By.XPATH, '//a[text()="Next"]')
            next_page_button.click()

            # Add a short delay to allow the next page to load
            time.sleep(2)  # Adjust the sleep duration as needed
        except Exception as e:
            # No next page button found or an error occurred, break out of the loop
            break

# Close the WebDriver
driver.quit()

# Print a message indicating the completion of scraping all pages
print(f"Data from all pages has been successfully scraped and saved to {csv_filename}")
