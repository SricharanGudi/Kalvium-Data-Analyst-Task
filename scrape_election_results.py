from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = "https://results.eci.gov.in"

driver = webdriver.Chrome()  

driver.get(url)

try:
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table-party") or contains(@id, "div1") or contains(@id, "dataTable")]'))
    )

    headers = [header.text.strip() for header in table.find_elements(By.TAG_NAME, 'th')]

    rows = []
    for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:  
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers)

  
    df.to_csv('election_results.csv', index=False)
    print("Election results have been saved to 'election_results.csv'")
except Exception as e:
    print("An error occurred:", str(e))
    elements = driver.find_elements(By.TAG_NAME, 'table')
    print(f"Found {len(elements)} tables on the page.")
    for i, element in enumerate(elements):
        print(f"Table {i+1}: {element.get_attribute('outerHTML')[:200]}...")  
finally:
    driver.quit()