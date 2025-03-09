import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def fetch_questions(topic):
    """
    Scrapes interview questions related to a topic.
    Uses BeautifulSoup first; falls back to Selenium if needed.
    """
    url = f"https://www.geeksforgeeks.org/tag/{topic}/"
    
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents bot detection

    try:
        # Attempt to scrape using requests & BeautifulSoup
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple ways to find questions (to handle site changes)
        question_elements = soup.find_all('h3') or soup.find_all('h2') or soup.find_all('p')
        questions = [q.text.strip() for q in question_elements[:5] if q.text.strip()]

        if questions:
            return questions  # Return scraped questions if found

    except requests.RequestException:
        pass  # Ignore errors & try Selenium instead

    # If BeautifulSoup fails, use Selenium (for JavaScript-heavy pages)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(url)
        question_elements = driver.find_elements(By.TAG_NAME, "h3") or driver.find_elements(By.TAG_NAME, "h2")
        questions = [q.text.strip() for q in question_elements if q.text.strip()]
        
        driver.quit()
        return questions if questions else []
    
    except Exception:
        return []  # Return empty list if both scraping methods fail
