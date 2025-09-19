import math
from fastapi import Depends, APIRouter
from asteval import Interpreter
import schemas
from typing import Deque, Annotated
from datetime import datetime
from dependencies import get_history, expand_percent

router = APIRouter(
    prefix="/calculate"
    # tags="calculate"
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

"""POST Calculate Route"""
@router.post("/")
def calculate(
    input: Annotated[dict, Depends(expand_percent)],
    history: Annotated[Deque, Depends(get_history)]
    ):
    try:
        expr = input["original"]
        code = input["expanded"]
        
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        
        """Add history """
        history.appendleft(schemas.ExpressionOut(
            timestamp=datetime.now().isoformat() + "Z",
            expr=expr,
            result=result))
        
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}
