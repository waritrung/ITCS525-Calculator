from fastapi import Depends, APIRouter
import schemas
from sqlmodel import Session, select
from fastapi import Depends
from database import get_session
from models import CalculatorLog, Session as CalcSession

router = APIRouter(
    prefix="/history"
    # tags="history"
)

HISTORY_MAX = 1000

"""GET hisory"""

@router.get("/")
def get(session: Session = Depends(get_session), limit: int = 50):
    logs = session.exec(select(CalculatorLog).order_by(CalculatorLog.id.desc())).all()
    return logs[: max(0, min(limit, HISTORY_MAX))]

"""DELETE history"""


@router.delete("/")
def clear(db: Session = Depends(get_session)):
    from sqlmodel import select
    # Delete all sessions (should cascade to logs)
    sessions = db.exec(select(CalcSession)).all()
    for s in sessions:
        db.delete(s)
    db.commit()
    return {"ok": True, "cleared": True}
