from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

# Specify the URL
url = "https://www.indiavotes.com/lok-sabha/2019/madhya-pradesh-[2000-onwards]/17/59"

# Set up Firefox WebDriver
driver = webdriver.Firefox()

# Open the website
driver.get(url)

# Scroll down to load the table content
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
time.sleep(2)  # Wait for the content to load (adjust the time if necessary)

# Get the HTML content after scrolling
html_content = driver.page_source

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the table element
table = soup.find("table")

# Extract data from the table
data = []
for row in table.find_all("tr")[1:]:  # Skip the header row
    columns = row.find_all("td")
    row_data = [col.get_text(strip=True) for col in columns]
    data.append(row_data)

# Close the WebDriver
driver.quit()

# Create a CSV file and write data to it
csv_filename = "indiavotes_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header
    header = [col.get_text(strip=True) for col in table.find_all("th")]
    csv_writer.writerow(header)
    # Write data rows
    csv_writer.writerows(data)

print(f"Data has been successfully scraped and saved to {csv_filename}")
