import base64
import hashlib
import random
import textwrap
from datetime import datetime

import pytz
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.x509 import load_der_x509_certificate
from django.conf import settings
from lxml import etree
from lxml.etree import Element, QName

from apps.sri.domain.enums import Methods, Namespaces


class XmlSigner:
    def __init__(self, cert, key):
        self.cert = cert
        self.key = key
        self.namespaces = {ns.name: ns.value for ns in Namespaces}

    def _get_token(self):
        return random.randint(1, 100000)

    def _build_identifiers(self):
        self.certificate_id = f"Certificate{self._get_token()}"
        self.signature_id = f"Signature{self._get_token()}"
        self.signed_properties_id = f"SignedProperties{self._get_token()}"
        self.object_id = f"Object{self._get_token()}"
        self.signed_info_id = f"Signature-SignedInfo{self._get_token()}"
        self.signed_propertiesID_id = f"SignedPropertiesID{self._get_token()}"
        self.referenceID_id = f"Reference-ID-{self._get_token()}"
        self.signature_value_id = f"SignatureValue{self._get_token()}"

    def _create_node(
        self, name, parent=None, ns="", tail=False, text=False, **node_attrs
    ):
        node = Element(QName(ns, name), nsmap=self.namespaces, **node_attrs)

        if parent is not None:
            parent.append(node)

        if tail:
            node.tail = tail

        if text:
            node.text = text

        return node

    def _get_object_node(self, cert_chain_digest):
        ds = Namespaces.ds.value
        etsi = Namespaces.etsi.value
        tz = pytz.timezone(settings.TIME_ZONE)
        signed_time = datetime.today().astimezone(tz)
        signed_time = signed_time.isoformat(timespec="seconds")

        certificate = load_der_x509_certificate(cert_chain_digest)
        cert_digest = hashlib.sha1(cert_chain_digest).digest()
        cert_b64 = base64.b64encode(cert_digest).decode()

        object = self._create_node(
            "Object", ns=ds, Id=f"{self.signature_id}-{self.object_id}"
        )
        quatifying_properties = self._create_node(
            "QualifyingProperties",
            parent=object,
            ns=etsi,
            Target=f"#{self.signature_id}",
        )
        signed_properties = self._create_node(
            "SignedProperties",
            parent=quatifying_properties,
            ns=etsi,
            Id=f"{self.signature_id}-{self.signed_properties_id}",
        )
        signed_signature_properties = self._create_node(
            "SignedSignatureProperties", parent=signed_properties, ns=etsi
        )
        self._create_node(
            "SigningTime", parent=signed_signature_properties, ns=etsi, text=signed_time
        )
        signing_certificate = self._create_node(
            "SigningCertificate", parent=signed_signature_properties, ns=etsi
        )
        cert = self._create_node("Cert", parent=signing_certificate, ns=etsi)
        cert_digest = self._create_node("CertDigest", parent=cert, ns=etsi)
        self._create_node(
            "DigestMethod",
            parent=cert_digest,
            ns=ds,
            Algorithm=Methods.digest.value,
        )
        self._create_node("DigestValue", parent=cert_digest, ns=ds, text=cert_b64)
        issuer_serial = self._create_node("IssuerSerial", parent=cert, ns=etsi)
        self._create_node(
            "X509IssuerName",
            parent=issuer_serial,
            ns=ds,
            text=certificate.issuer.rfc4514_string(),
        )
        self._create_node(
            "X509SerialNumber",
            parent=issuer_serial,
            ns=ds,
            text=str(certificate.serial_number),
        )

        signed_data_properties = self._create_node(
            "SignedDataObjectProperties", parent=signed_properties, ns=etsi
        )
        data_object_format = self._create_node(
            "DataObjectFormat",
            parent=signed_data_properties,
            ns=etsi,
            ObjectReference=f"#{self.referenceID_id}",
        )
        self._create_node(
            "Description",
            parent=data_object_format,
            ns=etsi,
            text="contenido comprobante",
        )
        self._create_node(
            "MimeType", parent=data_object_format, ns=etsi, text="text/xml"
        )

        signed_properties_c14n = etree.tostring(signed_properties, method="c14n")
        signed_properties_digest = hashlib.sha1(signed_properties_c14n).digest()
        signed_properties_b64 = base64.b64encode(signed_properties_digest).decode()

        return object, signed_properties_b64

    def _get_key_info_node(self, cert_chain_digest):
        ds = Namespaces.ds.value
        certificate = load_der_x509_certificate(cert_chain_digest)
        cert_chain = base64.b64encode(cert_chain_digest).decode()
        cert_chain = "\n".join(textwrap.wrap(cert_chain, 76))

        public_numbers = certificate.public_key().public_numbers()
        modulus = public_numbers.n
        modulus = modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder="big")
        modulus = base64.b64encode(modulus).decode()
        modulus = "\n".join(textwrap.wrap(modulus, 76))

        exponent = public_numbers.e
        exponent = exponent.to_bytes((exponent.bit_length() + 7) // 8, byteorder="big")
        exponent = base64.b64encode(exponent).decode()

        key_info = self._create_node(
            "KeyInfo", ns=ds, tail="\n", text="\n", Id=self.certificate_id
        )
        x509_data = self._create_node(
            "X509Data", parent=key_info, ns=ds, tail="\n", text="\n"
        )
        self._create_node(
            "X509Certificate",
            parent=x509_data,
            ns=ds,
            tail="\n",
            text=f"\n{cert_chain}\n",
        )

        key_value = self._create_node(
            "KeyValue", parent=key_info, ns=ds, tail="\n", text="\n"
        )
        rsa_key_value = self._create_node(
            "RSAKeyValue", parent=key_value, ns=ds, tail="\n", text="\n"
        )
        self._create_node(
            "Modulus", parent=rsa_key_value, ns=ds, tail="\n", text=f"\n{modulus}\n"
        )
        self._create_node(
            "Exponent", parent=rsa_key_value, ns=ds, tail="\n", text=exponent
        )

        key_info_c14n = etree.tostring(key_info, method="c14n")
        key_info_digest = hashlib.sha1(key_info_c14n).digest()
        key_info_b64 = base64.b64encode(key_info_digest).decode()

        return key_info, key_info_b64

    def _get_signed_info_node(self, signed_properties_b64, key_info_b64, voucher_b64):
        ds = Namespaces.ds.value
        signed_info = self._create_node(
            "SignedInfo", ns=ds, text="\n", tail="\n", Id=self.signed_info_id
        )
        self._create_node(
            "CanonicalizationMethod",
            parent=signed_info,
            tail="\n",
            ns=ds,
            Algorithm=Methods.canonicalization.value,
        )
        self._create_node(
            "SignatureMethod",
            parent=signed_info,
            ns=ds,
            tail="\n",
            Algorithm=Methods.signature.value,
        )
        ref_1 = self._create_node(
            "Reference",
            parent=signed_info,
            ns=ds,
            text="\n",
            tail="\n",
            Id=self.signed_propertiesID_id,
            Type="http://uri.etsi.org/01903#SignedProperties",
            URI=f"#{self.signature_id}-{self.signed_properties_id}",
        )
        self._create_node(
            "DigestMethod",
            parent=ref_1,
            ns=ds,
            tail="\n",
            Algorithm=Methods.digest.value,
        )
        self._create_node(
            "DigestValue", parent=ref_1, ns=ds, tail="\n", text=signed_properties_b64
        )

        ref_2 = self._create_node(
            "Reference",
            parent=signed_info,
            tail="\n",
            ns=ds,
            text="\n",
            URI=f"#{self.certificate_id}",
        )
        self._create_node(
            "DigestMethod",
            parent=ref_2,
            ns=ds,
            tail="\n",
            Algorithm=Methods.digest.value,
        )
        self._create_node(
            "DigestValue", parent=ref_2, ns=ds, tail="\n", text=key_info_b64
        )

        ref_3 = self._create_node(
            "Reference",
            parent=signed_info,
            ns=ds,
            text="\n",
            tail="\n",
            Id=self.referenceID_id,
            URI="#comprobante",
        )
        trasnforms = self._create_node(
            "Transforms", parent=ref_3, ns=ds, tail="\n", text="\n"
        )
        self._create_node(
            "Transform",
            parent=trasnforms,
            tail="\n",
            ns=ds,
            Algorithm=Methods.signature_construction.value,
        )
        self._create_node(
            "DigestMethod",
            parent=ref_3,
            ns=ds,
            tail="\n",
            Algorithm=Methods.digest.value,
        )
        self._create_node(
            "DigestValue", parent=ref_3, ns=ds, tail="\n", text=voucher_b64
        )

        return signed_info

    def _get_signature_value_node(self, private_key, signed_info):
        ds = Namespaces.ds.value
        signed_info_c14n = etree.tostring(signed_info, method="c14n")
        signed_info_signed = private_key.sign(
            signed_info_c14n, padding=PKCS1v15(), algorithm=hashes.SHA1()
        )
        signed_info_signed_b64 = base64.b64encode(signed_info_signed).decode()
        signed_info_signed_b64 = "\n".join(textwrap.wrap(signed_info_signed_b64, 76))

        signature_value = self._create_node(
            "SignatureValue",
            ns=ds,
            tail="\n",
            text=f"\n{signed_info_signed_b64}\n",
            Id=self.signature_value_id,
        )

        return signature_value

    def _get_signature_node(self, cert_digest, key_digest, voucher_b64):
        ds = Namespaces.ds.value
        private_key = load_der_private_key(key_digest, password=None)

        object, signed_properties_b64 = self._get_object_node(cert_digest)
        key_info, key_info_b64 = self._get_key_info_node(cert_digest)
        signed_info = self._get_signed_info_node(
            signed_properties_b64, key_info_b64, voucher_b64
        )
        signature_value = self._get_signature_value_node(private_key, signed_info)

        signature = self._create_node(
            "Signature", ns=ds, text="\n", Id=self.signature_id
        )
        signature.append(signed_info)
        signature.append(signature_value)
        signature.append(key_info)
        signature.append(object)

        return signature

    def sign(self, voucher_bytes) -> str:
        self._build_identifiers()
        cert_digest = base64.b64decode(self.cert)
        key_digest = base64.b64decode(self.key)

        voucher_root = etree.fromstring(voucher_bytes)
        voucher_c14n = etree.tostring(voucher_root, method="c14n")
        voucher_digest = hashlib.sha1(voucher_c14n).digest()
        voucher_b64 = base64.b64encode(voucher_digest).decode()

        signature = self._get_signature_node(cert_digest, key_digest, voucher_b64)
        voucher_root.append(signature)

        signed_voucher = etree.tostring(voucher_root, encoding="unicode")
        signed_voucher = '<?xml version="1.0" encoding="UTF-8"?>\n' + signed_voucher

        return signed_voucher
