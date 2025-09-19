from datetime import datetime
from pydantic import BaseModel, PositiveInt

class BaseExpression(BaseModel):
    expr: str
    
class ExpressionIn(BaseExpression):
    pass
    
class ExpressionOut(BaseExpression):
    ok: bool = True
    timestamp: str
    error: str = ""
    result: float = None