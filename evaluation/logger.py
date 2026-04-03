import json
import os
from datetime import datetime


LOG_FILE = "logs/evaluations.jsonl"


def log_evaluation(result):
    try:
        # ensure directory exists
        os.makedirs("logs", exist_ok=True)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": result.get("input"),
            "intent": result.get("intent"),
            "score": result.get("score", {}).get("final_score"),
            "errors": result.get("validation", {}).get("errors", []),
            "pass_errors": result.get("pass_validation", {}).get("errors", []),
            "feedback": result.get("feedback"),
            "suggestion": result.get("suggestion"),
        }

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception:
        # 🔴 NEVER break pipeline because of logging
        pass