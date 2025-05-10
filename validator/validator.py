import pandas as pd
from typing import List
from pydantic import ValidationError
from .schema import DailyEngagement

class DailyEngagementValidator:
    def __init__(self, path: str):
        self.path = path
        self.df = None
        self.registros_validados: List[DailyEngagement] = []

    def carregar_csv(self) -> pd.DataFrame:
        self.df = pd.read_csv(self.path)
        return self.df

    def validar(self) -> List[DailyEngagement]:
        if self.df is None:
            raise ValueError("CSV não carregado. Execute `carregar_csv` antes.")
        
        for idx, row in self.df.iterrows():
            try:
                registro = DailyEngagement(**row.to_dict())
                self.registros_validados.append(registro)
            except ValidationError as e:
                print(f"Erro de validação na linha {idx}: {e}")
        
        return self.registros_validados
