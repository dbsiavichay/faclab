from datetime import datetime, timedelta

import pytest
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, pkcs12
from cryptography.x509.oid import NameOID


@pytest.fixture
def signature_file_p12():
    password = "password"
    subject_name = "TEST SUBJECT"
    serial_number = x509.random_serial_number()
    issue_date = datetime.now().replace(microsecond=0)
    expiry_date = issue_date + timedelta(days=365)

    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "EC"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Test provice"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Test locality"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test"),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(serial_number)
        .not_valid_before(issue_date)
        .not_valid_after(expiry_date)
        .sign(key, hashes.SHA256(), default_backend())
    )
    metadata = {
        "subject_name": subject_name,
        "serial_number": serial_number,
        "issue_date": issue_date,
        "expiry_date": expiry_date,
    }

    p12 = pkcs12.serialize_key_and_certificates(
        b"signing key", key, cert, None, BestAvailableEncryption(password.encode())
    )

    return p12, password, metadata
