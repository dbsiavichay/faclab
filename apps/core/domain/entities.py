from typing import Optional

from pydantic import BaseModel, Field, computed_field


class SRIConfig(BaseModel):
    code: str = Field(max_length=13)
    company_name: str
    trade_name: str
    main_address: str
    company_address: str
    company_code: str = Field(max_length=4)
    company_point_sale_code: str = Field(max_length=4)
    special_taxpayer_resolution: Optional[str]
    withholding_agent_resolution: Optional[str]
    accounting_required: Optional[bool]
    environment: str  # TODO: add choices
    emission: str  # TODO: add choices
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
