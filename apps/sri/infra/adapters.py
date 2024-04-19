import base64

from django.utils.translation import gettext_lazy as _
from zeep import Client

from apps.sri.domain.entities import (
    AuthorizationResponse,
    AuthorizationResult,
    VoucherResponse,
)
from apps.sri.domain.ports import SRIVoucherPort


class SRIVoucherAdapter(SRIVoucherPort):
    def __init__(self, voucher_client: Client, authorization_client: Client) -> None:
        self.voucher_client = voucher_client
        self.authorization_client = authorization_client

    def send_voucher(self, voucher: bytes) -> bool:
        response = None

        try:
            data = base64.encodebytes(voucher).decode("utf-8")
            res = self.voucher_client.service.validarComprobante(data)
            response = VoucherResponse(**res.__dict__["__values__"])
        except Exception as e:
            message = _("SRI ERROR on send voucher")
            raise Exception(f"{message}: {e}")

        if response and response.status == "DEVUELTA":
            msgs = [
                f"{msg.text} ** {msg.additional_info}"
                for msg in response.results[0].messages
            ]
            message = _("SRI ERROR voucher rejected") + " * ".join(msgs)
            raise Exception(message)

        return True

    def retrieve_voucher_by_access_code(self, access_code: str) -> AuthorizationResult:
        response = None

        try:
            res = self.authorization_client.service.autorizacionComprobante(access_code)
            response = AuthorizationResponse(**res.__dict__["__values__"])
        except Exception as e:
            error = _("SRI ERROR on fetch voucher")
            raise Exception(f"{error}: {e}")

        if response and not response.results_count:
            error = _("SRI ERROR no vouchers found for code")
            raise Exception(f"{error} {response.access_code}")

        authorized_vouchers = [v for v in response.results if v.status == "AUTORIZADO"]

        if not authorized_vouchers:
            msgs = [
                f"{msg.text} ** {msg.additional_info}"
                for msg in response.results[0].messages
            ]
            error = _("SRI ERROR on validation") + " ** ".join(msgs)
            raise Exception(error)

        return authorized_vouchers[0]
