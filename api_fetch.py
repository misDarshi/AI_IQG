import requests
import time

last_api_call = 0  # Track last API request time

def get_leetcode_question():
    """
    Fetches a coding interview question from LeetCode API.
    Implements rate limiting to avoid being blocked.
    """
    global last_api_call
    if time.time() - last_api_call < 5:  # Wait at least 5 sec before next call
        return None  

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
        last_api_call = time.time()  # Update last API call time
        
        if data and "problemsetQuestionList" in data["data"]:
            question = data["data"]["problemsetQuestionList"]["questions"][0]
            return f"{question['title']} ({question['difficulty']})"
    except requests.RequestException:
        return None  # Return None if API call fails
