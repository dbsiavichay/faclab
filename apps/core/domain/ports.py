from abc import ABC, abstractmethod
from typing import List

from apps.core.domain.entities import UploadFile


class SealifyPort(ABC):
    @abstractmethod
    def create_certificate(self, certificate: UploadFile, password: str) -> dict:
        pass

    @abstractmethod
    def list_certificates(self) -> List[dict]:
        pass

    @abstractmethod
    def delete_certificate(self, certificate_id: str) -> None:
        pass

    @abstractmethod
    def seal_invoice(self, invoice_xml: str, certificate_id: str) -> str:
        pass
