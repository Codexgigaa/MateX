from pydantic import BaseModel,Field
from datetime import datetime

class Message(BaseModel):
    role : str
    text : str
    timestamp : datetime = Field(default_factory = datetime.now)
user = Message(
    role = "User",
    text = "Hi ji",
    timestamp = datetime.now()
)
# testing
# print(user)
# print("code pass")