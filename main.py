import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Load the Falcon-7B model for generating AI-based questions
generator = pipeline("text-generation", model="tiiuae/falcon-7b")

def gen_iq(topic):
    """
    Generates an AI-based interview question using Falcon-7B.
    Used as a last fallback if web scraping & API both fail.
    """
    prompt = f"Generate a technical interview question related to {topic}:"
    response = generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]

# ---------------------- WEB SCRAPING FUNCTION ----------------------
def fetch_questions(topic):
    """
    Scrapes interview questions related to a topic from GeeksforGeeks.
    Adapts to minor website changes to prevent breakage.
    """
    url = f"https://www.geeksforgeeks.org/tag/{topic}/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents bot detection

    try:
        response = requests.get(url, headers=headers, timeout=5)  # Timeout to handle site issues
        response.raise_for_status()
    except requests.RequestException:
        return []  # Return empty list if scraping fails

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try multiple element tags to adapt to site changes
    question_elements = soup.find_all('h3') or soup.find_all('h2') or soup.find_all('p')
    
    questions = [q.text.strip() for q in question_elements[:5] if q.text.strip()]
    return questions if questions else []  # Return scraped questions if available

# ---------------------- API FUNCTION (LeetCode) ----------------------
def get_leetcode_question():
    """
    Fetches a coding interview question from LeetCode API.
    Used if web scraping fails.
    """
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        {
            problemsetQuestionList(
                categorySlug: ""
                filters: {}
                limit: 1
            ) {
                questions {
                    title
                    difficulty
                }
            }
        }
        """
    }

    try:
        response = requests.post(url, json=query, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data and "problemsetQuestionList" in data["data"]:
            question = data["data"]["problemsetQuestionList"]["questions"][0]
            return f"{question['title']} ({question['difficulty']})"
    except requests.RequestException:
        return None  # Return None if API call fails

# ---------------------- MASTER FUNCTION: DECIDES BEST METHOD ----------------------
def get_dynamic_question(topic):
    """
    Tries web scraping first, falls back to API if scraping fails, 
    and uses AI model as a final fallback.
    """
    questions = fetch_questions(topic)
    
    if questions:
        return questions[0]  # Return first scraped question
    
    question = get_leetcode_question()
    
    if question:
        return question  # Return API question
    
    return gen_iq(topic)  # Use AI model as final fallback

# ---------------------- MAIN PROGRAM ----------------------
if __name__ == "__main__":
    topic = input("Enter a topic: ")  # User enters topic dynamically
    question = get_dynamic_question(topic)
    print(f"Generated Interview Question: {question}")
