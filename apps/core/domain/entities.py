from typing import Optional

from pydantic import BaseModel, computed_field


class SRIConfig(BaseModel):
    iva_percent: Optional[float]
    signature: Optional[int]

    @computed_field
    def iva_rate(self) -> float:
        return self.iva_percent / 100 if self.iva_percent else None

    @computed_field
    def iva_factor(self) -> float:
        return (self.iva_percent / 100) + 1 if self.iva_percent else None


class SiteEntity(BaseModel):
    id: int
    sri_config: SRIConfig
