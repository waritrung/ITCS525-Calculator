
import re
from datetime import datetime
from typing import Any
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

# _percent_pair = re.compile(r"""
#     (?P<a>\d+(?:\.\d+)?)
#     \s*(?P<op>[+\-*/])\s*
#     (?P<b>\d+(?:\.\d+)?)%
# """, re.VERBOSE)
# _number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")


class Expression(SQLModel):
    pass
    # expr: str

    # def expand_percent(self) -> str:
    #     """Handle A op B% and standalone N% patterns."""
    #     s = self.expr
    #     while True:
    #         # Replace A op B%
    #         m = _percent_pair.search(s)
    #         if not m:
    #             break
    #         a, op, b = m.group("a", "op", "b")
    #         if op in "+-":
    #             repl = f"{a} {op} (({b}/100)*{a})"
    #         elif op == "*":
    #             repl = f"{a} * ({b}/100)"
    #         else:
    #             repl = f"{a} / ({b}/100)"
    #         s = s[:m.start()] + repl + s[m.end():]

    #     # Replace B%
    #     s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
    #     return s



class Session(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    started_at: str
    ended_at: str | None = None
    logs: list["CalculatorLog"] = Relationship(back_populates="session")


class CalculatorLog(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    expr: str
    timestamp: str = datetime.now().isoformat() + "Z"
    ok: bool = True
    error: str = ""
    result: float = None
    session_id: int | None = Field(default=None, foreign_key="session.id")
    session: Session | None = Relationship(back_populates="logs")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None = None