from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime

class DailyEngagement(BaseModel):
    user_id: str
    video_id: str
    category: str
    view_start_time: Optional[datetime]
    view_end_time: Optional[datetime]
    region: Optional[str]

    @field_validator("user_id", "video_id", "category")
    def campo_obrigatorio(cls, v, info):
        if not v or str(v).strip() == "":
            raise ValueError(f"{info.field_name} não pode estar vazio")
        return v

    @field_validator("region")
    def validar_region(cls, v):
        if v is None:
            return v
        if len(v) != 2:
            raise ValueError("Região deve ter 2 caracteres")
        return v

    @model_validator(mode="after")
    def validar_intervalo_tempo(self):
        if self.view_start_time and self.view_end_time:
            if self.view_end_time < self.view_start_time:
                raise ValueError("view_end_time deve ser posterior a view_start_time")
        return self