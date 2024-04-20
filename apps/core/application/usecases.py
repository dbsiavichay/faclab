import base64
import os
import subprocess
from tempfile import NamedTemporaryFile
from uuid import uuid4

import jks
import pytz
from cryptography.x509 import load_der_x509_certificate
from cryptography.x509.oid import NameOID
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.core.domain.entities import SignatureEntity

from .exceptions import SignatureException


class RetrieveSignatureUseCase:
    def execute(self, p12_data: bytes, password: str) -> SignatureEntity:
        p12_file = NamedTemporaryFile(suffix=".p12")

        with open(p12_file.name, "wb") as file:
            file.write(p12_data)

        try:
            keystore_name = f"{uuid4()}.jks"
            command = settings.KEYTOOL_COMMAND.format(
                p12_file.name, keystore_name, password, password
            )
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
            )
            print(f"Success run command {output}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Return code: {e.returncode}")
            print(f"Output: {e.output}")
            raise SignatureException(_("error while call keytool command").capitalize())

        ks = jks.KeyStore.load(keystore_name, password)
        keys = [k for k in ks.private_keys.values() if "signing key" in k.alias]
        os.remove(keystore_name)

        if not keys:
            raise SignatureException(
                _("signature file has not valid keys").capitalize()
            )

        key = keys.pop()

        if not key.is_decrypted():
            key.decrypt(password)

        cert_digest = key.cert_chain[0][1]
        cert = base64.b64encode(cert_digest).decode()
        key = base64.b64encode(key.pkey).decode()
        certificate = load_der_x509_certificate(cert_digest)
        subject = certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        signature_entity = SignatureEntity(
            **{
                "subject_name": subject[0].value,
                "serial_number": certificate.serial_number,
                "issue_date": certificate.not_valid_before.astimezone(pytz.utc),
                "expiry_date": certificate.not_valid_after.astimezone(pytz.utc),
                "cert": cert,
                "key": key,
            }
        )

        return signature_entity
