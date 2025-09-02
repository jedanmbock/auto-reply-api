from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    
class Data(BaseModel):
    message: str
    user: User

class RawData(BaseModel):
    source: str
    data: Data