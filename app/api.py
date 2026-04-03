from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
import time

from app.main import run_pipeline

app = FastAPI(title="COS Reasoning Evaluator API")


# 🔴 Request Schema (Single)
class InputText(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


# 🔴 Batch Schema
class BatchInput(BaseModel):
    texts: list[str] = Field(..., min_items=1, max_items=50)


# 🔴 Health Check
@app.get("/")
def home():
    return {"message": "COS API is running"}


# 🔴 Core Safe Execution (SINGLE CALL ONLY)
def execute_pipeline(text: str):
    start_time = time.time()

    try:
        full_result = run_pipeline(text)

        clean_result = {
            "input": full_result.get("input", text),
            "intent": full_result.get("intent", "unknown"),
            "score": full_result.get("score", {}).get("final_score", 0.0),
            "feedback": full_result.get("feedback", []),
            "suggestion": full_result.get("suggestion", None),
            "meta": {
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "status": "success"
            }
        }

        return full_result, clean_result

    except Exception as e:
        error_result = {
            "input": text,
            "intent": "unknown",
            "score": 0.0,
            "feedback": [{
                "type": "system",
                "message": "Internal error during evaluation"
            }],
            "suggestion": None,
            "meta": {
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "status": "error",
                "error": str(e)
            }
        }

        return None, error_result


# 🔴 SINGLE INPUT ENDPOINT
@app.post("/evaluate")
def evaluate(input_data: InputText, debug: bool = Query(False)):

    full_result, clean_result = execute_pipeline(input_data.text)

    if debug:
        return {
            "clean": clean_result,
            "debug": full_result if full_result else {}
        }

    return clean_result


# 🔴 BATCH ENDPOINT
@app.post("/evaluate-batch")
def evaluate_batch(input_data: BatchInput, debug: bool = Query(False)):

    results = []

    for text in input_data.texts:

        full_result, clean_result = execute_pipeline(text)

        if debug:
            results.append({
                "clean": clean_result,
                "debug": full_result if full_result else {}
            })
        else:
            results.append(clean_result)

    return {
        "count": len(results),
        "results": results
    }