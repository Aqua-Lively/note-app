from typing import Optional

from pydantic import BaseModel, ConfigDict

class SNoteAdd(BaseModel):
    text: str


class SNote(SNoteAdd):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
