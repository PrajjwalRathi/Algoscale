from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup for Selenium to use ChromeDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def findTotalArticlesByLanguages(languages):
    url = "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table"
    driver = get_driver()
    
    driver.get(url)
    
    time.sleep(5)
    
    tables = driver.find_elements(By.XPATH, "//table[contains(@class, 'sortable')]")
    table = tables[0]
    
    rows = table.find_elements(By.XPATH, ".//tr")[1:]
    
    total_articles = 0
    
    for row in rows:
        columns = row.find_elements(By.XPATH, ".//td")
        if len(columns) > 4:
            language_name = columns[1].text.strip()
            articles = columns[4].text.strip()

            if language_name in languages:
                try:
                    total_articles += int(articles.replace(',', ''))
                except ValueError:
                    continue
    
    driver.quit()
    
    return total_articles

languages = ["Arabic", "Portuguese"]
total = findTotalArticlesByLanguages(languages)
print(f"Total articles for {languages}: {total}")
