from abc import ABC, abstractmethod

from .entities import AuthorizationResult


class SRIVoucherPort(ABC):
    @abstractmethod
    def send_voucher(self, voucher: bytes) -> bool:
        pass

    @abstractmethod
    def retrieve_voucher_by_access_code(self, access_code: str) -> AuthorizationResult:
        pass
