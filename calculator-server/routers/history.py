from fastapi import Depends, APIRouter
import schemas
from typing import Deque, Annotated
from dependencies import get_history

router = APIRouter(
    prefix="/history"
    # tags="history"
)

HISTORY_MAX = 1000

"""GET hisory"""
@router.get("/")
def get(
    history: Annotated[Deque, Depends(get_history)],limit: int = 50) -> list[schemas.ExpressionOut]:
    return list(history)[: max(0, min(limit, HISTORY_MAX))]

"""DELETE history"""
@router.delete("/")
def clear(
    history: Annotated[Deque, Depends(get_history)]
):
    history.clear()
    return {"ok": True, "cleared": True}
