from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
import time

from app.main import run_pipeline


app = FastAPI(title="COS Reasoning Evaluator API")


# 🔴 Request Schema
class InputText(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


# 🔴 Health Check
@app.get("/")
def home():
    return {"message": "COS API is running"}


# 🔴 SAFE EXECUTION WRAPPER
def safe_run(text: str):
    start_time = time.time()

    try:
        result = run_pipeline(text)

        # enforce structure (no missing keys)
        safe_result = {
            "input": result.get("input", text),
            "intent": result.get("intent", "unknown"),
            "score": result.get("score", {}).get("final_score", 0.0),
            "feedback": result.get("feedback", []),
            "suggestion": result.get("suggestion", None),
            "meta": {
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "status": "success"
            }
        }

        return safe_result

    except Exception as e:
        return {
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


# 🔴 Core Endpoint
@app.post("/evaluate")
def evaluate(input_data: InputText, debug: bool = Query(False)):

    result = safe_run(input_data.text)

    if debug:
        # full pipeline (unsafe but useful)
        try:
            full = run_pipeline(input_data.text)
            return {
                "clean": result,
                "debug": full
            }
        except:
            return result

    return result


# 🔴 Batch Input
class BatchInput(BaseModel):
    texts: list[str] = Field(..., min_items=1, max_items=50)


@app.post("/evaluate-batch")
def evaluate_batch(input_data: BatchInput, debug: bool = Query(False)):

    results = []

    for text in input_data.texts:
        result = safe_run(text)

        if debug:
            try:
                full = run_pipeline(text)
                results.append({
                    "clean": result,
                    "debug": full
                })
            except:
                results.append(result)
        else:
            results.append(result)

    return {
        "count": len(results),
        "results": results
    }