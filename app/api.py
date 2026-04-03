from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel

from app.main import run_pipeline


app = FastAPI(title="COS Reasoning Evaluator API")


# 🔴 Request Schema
class InputText(BaseModel):
    text: str


# 🔴 Health Check
@app.get("/")
def home():
    return {"message": "COS API is running"}

# 🔴 Core Endpoint
@app.post("/evaluate")
def evaluate(input_data: InputText, debug: bool = Query(False)):

    result = run_pipeline(input_data.text)

    # 🔴 DEBUG MODE
    if debug:
        return result

    # 🔴 USER MODE
    clean_response = {
        "input": result.get("input"),
        "intent": result.get("intent"),
        "score": result.get("score", {}).get("final_score"),
        "feedback": result.get("feedback"),
        "suggestion": result.get("suggestion")
    }

    return clean_response

class BatchInput(BaseModel):
    texts: list[str]

@app.post("/evaluate-batch")
def evaluate_batch(input_data: BatchInput, debug: bool = Query(False)):

    results = []

    for text in input_data.texts:
        result = run_pipeline(text)

        if debug:
            results.append(result)
        else:
            clean = {
                "input": result.get("input"),
                "intent": result.get("intent"),
                "score": result.get("score", {}).get("final_score"),
                "feedback": result.get("feedback"),
                "suggestion": result.get("suggestion")
            }
            results.append(clean)

    return {
        "count": len(results),
        "results": results
    }