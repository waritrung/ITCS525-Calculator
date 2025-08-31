import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

"""POST Calculate Route"""
@app.post("/calculate")
def calculate(expr: str):
    try:
        
        expr = expr.replace("×", "*")
        expr = expr.replace("÷", "/")

        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        
        """Add history """
        history.appendleft({
            "timestamp": datetime.now().isoformat() + "Z",
            "expr": expr,
            "result": result,
        })
        
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}

"""GET hisory"""
@app.get("/history")
def get_history(limit: int = 50):
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


"""DELETE history"""
@app.delete("/history")
def clear_History():
    history.clear()
    return {"ok": True, "cleared": True}
