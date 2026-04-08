from pydantic import BaseModel

class FactoryAction(BaseModel):
    action_type: str