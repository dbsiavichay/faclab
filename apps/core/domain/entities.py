from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field

from .enums import EmissionTypeEnum, EnvironmentEnum


class SRIConfig(BaseModel):
    company_code: str = Field(max_length=13)
    company_name: str
    company_trade_name: str
    company_main_address: str
    company_branch_address: str
    company_branch_code: str = Field(max_length=4)
    company_sale_point_code: str = Field(max_length=4)
    special_taxpayer_resolution: Optional[str]
    withholding_agent_resolution: Optional[str]
    company_accounting_required: Optional[bool]
    environment: EnvironmentEnum
    emission_type: EmissionTypeEnum
    iva_fee: Optional[int]
    iva_percent: Optional[float]
    signature: Optional[str]

    @computed_field
    def iva_rate(self) -> float:
        return self.iva_percent / 100 if self.iva_percent else None

    @computed_field
    def iva_factor(self) -> float:
        return (self.iva_percent / 100) + 1 if self.iva_percent else None


class SiteEntity(BaseModel):
    id: int
    sri_config: SRIConfig


class CertificateEntity(BaseModel):
    id: str
    subject_name: str = Field(alias="subjectName")
    serial_number: int = Field(alias="serialNumber")
    issue_date: datetime = Field(alias="issueDate")
    expiry_date: datetime = Field(alias="expiryDate")


class SealedInvoice(BaseModel):
    sealed_data: str = Field(alias="sealedData")


class UploadFile(BaseModel):
    file: bytes
    filename: str
    content_type: str
