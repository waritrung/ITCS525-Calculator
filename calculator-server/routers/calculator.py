import math
from fastapi import Depends, APIRouter
from asteval import Interpreter
import schemas

from typing import Annotated
from datetime import datetime, timedelta
from dependencies import expand_percent
from sqlmodel import Session, select
from fastapi import Depends
from database import get_session
from models import CalculatorLog, Session as CalcSession

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
    db: Session = Depends(get_session)
    ):
    expr = input["original"]
    code = input["expanded"]
    now = datetime.now()

    # Find latest session
    latest_session = db.exec(select(CalcSession).order_by(CalcSession.id.desc())).first()
    session_to_use = None
    if latest_session:
        # Find latest log in that session
        latest_log = db.exec(
            select(CalculatorLog)
            .where(CalculatorLog.session_id == latest_session.id)
            .order_by(CalculatorLog.id.desc())
        ).first()
        last_time = None
        if latest_log:
            last_time = datetime.fromisoformat(latest_log.timestamp.rstrip('Z'))
        else:
            last_time = datetime.fromisoformat(latest_session.started_at.rstrip('Z'))
        if (now - last_time).total_seconds() > 10:
            # End old session
            latest_session.ended_at = now.isoformat() + "Z"
            db.add(latest_session)
            db.commit()
            # Create new session
            session_to_use = CalcSession(name=f"Session {now:%Y-%m-%d %H:%M:%S}", started_at=now.isoformat() + "Z")
            db.add(session_to_use)
            db.commit()
            db.refresh(session_to_use)
        else:
            session_to_use = latest_session
    else:
        # No session exists, create one
        session_to_use = CalcSession(name=f"Session {now:%Y-%m-%d %H:%M:%S}", started_at=now.isoformat() + "Z")
        db.add(session_to_use)
        db.commit()
        db.refresh(session_to_use)

    try:
        result = aeval(code)
        error = ""
        ok = True
        if aeval.error:
            error = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            ok = False
        log = CalculatorLog(
            expr=expr,
            timestamp=now.isoformat() + "Z",
            ok=ok,
            error=error,
            result=result if ok else None,
            session_id=session_to_use.id
        )
        db.add(log)
        db.commit()
        return {"ok": ok, "expr": expr, "result": result if ok else None, "error": error}
    except Exception as e:
        log = CalculatorLog(
            expr=expr,
            timestamp=now.isoformat() + "Z",
            ok=False,
            error=str(e),
            result=None,
            session_id=session_to_use.id
        )
        db.add(log)
        db.commit()
        return {"ok": False, "expr": expr, "error": str(e)}
