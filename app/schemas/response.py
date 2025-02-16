from pydantic import BaseModel,Field
from datetime import datetime,timezone

class ApiResponse(BaseModel):
    message : str
    success : bool = True 
    timestamp : str = Field(default_factory=lambda:datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
    data : dict = {}
    http_status : int = 200