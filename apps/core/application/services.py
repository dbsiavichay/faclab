from apps.core.application.usecases import RetrieveSignatureUseCase
from apps.core.domain.entities import SignatureEntity
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
