from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):
    def __init__(self, message: str, success: bool = True, timestamp: datetime = datetime.now(), data: dict = {}, http_status: int = 200):
        self.message = message
        self.success = success
        self.timestamp = timestamp
        self.data = data
        self.http_status = http_status