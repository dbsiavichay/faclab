from typing import List

from apps.core.application.usecases import RetrieveSignatureUseCase
from apps.core.domain.entities import (
    CertificateEntity,
    SealedInvoice,
    SignatureEntity,
    UploadFile,
)
from apps.core.domain.ports import SealifyPort
from apps.core.domain.repositories import SignatureRepository


class SignatureService:
    def __init__(
        self,
        signature_repository: SignatureRepository,
        retrieve_signature_usecase: RetrieveSignatureUseCase,
    ) -> None:
        self.signature_repository = signature_repository
        self.retrieve_signature_usecase = retrieve_signature_usecase

    def retrieve_signature(self, p12_data: bytes, password: str) -> SignatureEntity:
        return self.retrieve_signature_usecase.execute(p12_data, password)


class SealifyService:
    def __init__(self, sealify_port: SealifyPort) -> None:
        self.sealify_port = sealify_port

    def create_certificate(
        self, certificate: UploadFile, password: str
    ) -> CertificateEntity:
        data = self.sealify_port.create_certificate(certificate, password)
        return CertificateEntity(**data)

    def list_certificates(self) -> List[CertificateEntity]:
        data = self.sealify_port.list_certificates()
        return [CertificateEntity(**item) for item in data]

    def delete_certificate(self, certificate_id: str) -> None:
        self.sealify_port.delete_certificate(certificate_id)

    def seal_invoice(self, invoice_xml: str, certificate_id: str) -> SealedInvoice:
        data = self.sealify_port.seal_invoice(invoice_xml, certificate_id)
        return SealedInvoice(**data)
