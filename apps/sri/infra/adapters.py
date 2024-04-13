import base64

from django.utils.translation import gettext_lazy as _
from zeep import Client

from apps.sri.domain.entities import VoucherAPIResponse, VoucherEntity
from apps.sri.domain.ports import SRIVoucherPort


class SRIVoucherAdapter(SRIVoucherPort):
    def __init__(self, sending_client: Client, query_client: Client) -> None:
        self.sending_client = sending_client
        self.query_client = query_client

    def send_voucher(self, voucher_entity: VoucherEntity) -> None:
        FAIL_STATUS = "DEVUELTA"

        try:
            data = base64.encodebytes(voucher_entity.file).decode("utf-8")
            result = self.sending_client.service.validarComprobante(data)
        except Exception as e:
            message = _("SRI Error to send voucher")
            raise Exception(f"{message}: {e}")

        if result.estado == FAIL_STATUS:
            messages = [
                mensaje.mensaje.capitalize()
                for mensaje in result.comprobantes.comprobante[0].mensajes.mensaje
            ]
            message = _("SRI Voucher not received") + " * ".join(messages)
            raise Exception(message)

    def retrieve_voucher_by_access_code(self, access_code: str) -> VoucherEntity:
        response = None

        try:
            res = self.query_client.service.autorizacionComprobante(access_code)
            response = VoucherAPIResponse(**res.__dict__["__values__"])
        except Exception as e:
            error = _("SRI ERROR on fetch voucher")
            raise Exception(f"{error}: {e}")

        if response and not response.vouchers_count:
            error = _("SRI ERROR No vouchers found for code")
            raise Exception(f"{error} {response.queried_code}")

        authorized_vouchers = [v for v in response.vouchers if v.status == "AUTORIZADO"]

        if not authorized_vouchers:
            msgs = [
                f"{msg.text} ** {msg.additional_info}"
                for msg in response.vouchers[0].messages
            ]
            error = _("SRI ERROR on validation") + " ** ".join(msgs)
            raise Exception(error)

        return VoucherEntity(
            code=response.queried_code,
            file=authorized_vouchers[0].voucher_xml,
            authorization_date=authorized_vouchers[0].authorization_date,
        )
