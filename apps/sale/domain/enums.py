from enum import Enum


class VoucherStatusEnum(str, Enum):
    GENERATED = "gen"
    SIGNED = "sig"
    VALIDATED = "val"
    AUTHORIZED = "aut"


class PaymentTypeEnum(str, Enum):
    CASH = "01"
    CREDIT_CARD = "19"
    BANK = "20"
