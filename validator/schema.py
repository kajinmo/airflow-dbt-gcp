from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime

class DailyEngagement(BaseModel):
    """
    Data model for engagement records
    """
    user_id: str
    video_id: str
    category: str
    view_start_time: Optional[datetime]
    view_end_time: Optional[datetime]
    region: Optional[str]


    @field_validator("user_id", "video_id", "category")
    def validate_required_fields(cls, value, field):
        if not value or not str(value).strip():
            raise ValueError(f"{field} cannot be empty")
        return value


    @field_validator("region")
    def validate_region(cls, value):
        if value is None:
            return value
        if len(value) != 2 or not value.isalpha() or not value.isupper():
            raise ValueError("Region must be 2 uppercase letters (e.g., 'US', 'BR')")
        return value


    @model_validator(mode="after")
    def validar_intervalo_tempo(self):
        if self.view_start_time and self.view_end_time:
            if self.view_end_time < self.view_start_time:
                raise ValueError("view_end_time must be after a view_start_time")
        return self