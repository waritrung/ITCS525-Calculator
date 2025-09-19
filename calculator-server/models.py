from datetime import datetime
from pydantic import BaseModel, PositiveInt

class Expression(BaseModel):
    expr: str
    
class CalculatorLog(BaseModel):
    ok: bool = True
    timestamp: str
    expr: str
    error: str = ""
    result: float = None