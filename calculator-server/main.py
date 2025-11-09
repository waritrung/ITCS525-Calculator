from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import calculator,history
from database import engine, get_session
from sqlmodel import SQLModel, select
from contextlib import asynccontextmanager
from models import User




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown code

app = FastAPI(title="Mini Calculator API", lifespan=lifespan)

app.include_router(calculator.router)
app.include_router(history.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users")
def read_users(session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# # ---------- Safe evaluator ----------
# aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

# """POST Calculate Route"""
# @app.post("/calculate")
# def calculate(
#     input: Annotated[schemas.ExpressionIn, Depends(expand_percent)],
#     history: Annotated[Deque, Depends(get_history)]
#     ):
#     try:
        
#         result = aeval(input.expr)
#         if aeval.error:
#             msg = "; ".join(str(e.get_error()) for e in aeval.error)
#             aeval.error.clear()
#             return {"ok": False, "expr": input.expr, "result": "", "error": msg}
        
#         """Add history """
#         history.appendleft(schemas.ExpressionOut(
#             timestamp=datetime.now().isoformat() + "Z",
#             expr=input.expr,
#             result=result))
        
#         return {"ok": True, "expr": input.expr, "result": result, "error": ""}
#     except Exception as e:
#         return {"ok": False, "expr": input.expr, "error": str(e)}

# """GET hisory"""
# @app.get("/history")
# def get(
#     history: Annotated[Deque, Depends(get_history)],limit: int = 50) -> list[schemas.ExpressionOut]:
#     return list(history)[: max(0, min(limit, HISTORY_MAX))]

# """DELETE history"""
# @app.delete("/history")
# def clear(
#     history: Annotated[Deque, Depends(get_history)]
# ):
#     history.clear()
#     return {"ok": True, "cleared": True}
