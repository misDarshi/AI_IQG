from fastapi import FastAPI
from main import get_dynamic_question  # Import your function

app = FastAPI()  # Create API instance

@app.get("/generate/")
def generate_question(topic: str):
    """
    API endpoint to generate an interview question.
    Example: GET /generate/?topic=Data Structures
    """
    question = get_dynamic_question(topic)
    return {"topic": topic, "question": question}

