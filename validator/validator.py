import pandas as pd
from typing import List
from pydantic import ValidationError
from .schema import DailyEngagement

class EngagementValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.valid_records: List[DailyEngagement] = []
        self.errors: List[dict] = []

    def validate(self) -> List[DailyEngagement]:
        """Validate all records in the DataFrame"""
        for idx, row in self.df.iterrows():
            try:
                record = DailyEngagement(**row.to_dict())
                self.valid_records.append(record)
            except ValidationError as e:
                self._log_error(idx, e)
        return self.valid_records

    def _log_error(self, row_index: int, error: ValidationError):
        self.errors.append({
            "row": row_index,
            "error": str(error),
            "data": self.df.iloc[row_index].to_dict()
        })