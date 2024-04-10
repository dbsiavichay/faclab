from abc import ABC, abstractmethod

from .entities import VoucherEntity


class SRIVoucherPort(ABC):
    @abstractmethod
    def send_voucher(self, voucher_entity: VoucherEntity) -> None:
        pass

    @abstractmethod
    def retrieve_voucher_by_code(self, code: str) -> VoucherEntity:
        pass
