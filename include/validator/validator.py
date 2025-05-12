import pandas as pd
import logging
from typing import List
from pydantic import ValidationError
from .schema import DailyEngagement

class EngagementValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.valid_data = []
        self.errors = []
        self.logger = logging.getLogger(__name__)


    def validate(self) -> List[DailyEngagement]:
        """
        Validate all records in the DataFrame
        """
        self.logger.info(f"Starting validation of {len(self.df)} records")
        for idx, row in self.df.iterrows():
            try:
                model = DailyEngagement(**row.to_dict())
                self.valid_data.append(model.dict())
            except ValidationError as e:
                self._log_error(idx, e)
        self.logger.info(
            f"Validation complete. {len(self.valid_data)} valid, "
            f"{len(self.errors)} invalid records"
        )
        return self.valid_data


    def get_valid_dataframe(self) -> pd.DataFrame:
        """
        Converts valid records (Pydantic models) back to a DataFrame
        """
        return pd.DataFrame([record.model_dump() for record in self.valid_data])
    

    def _log_error(self, row_index: int, error: ValidationError):
        """
        Logs and stores validation error details (row number, error message, and row data) for later reporting
        """
        error_data = {
            "row": row_index,
            "error": str(error),
            "data": self.df.iloc[row_index].to_dict()
        }
        self.errors.append(error_data)
        self.logger.warning(
            f"Validation error on row {row_index}: {str(error)}"
        )