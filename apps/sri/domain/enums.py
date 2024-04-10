from enum import Enum


class Namespaces(Enum):
    ds = "http://www.w3.org/2000/09/xmldsig#"
    etsi = "http://uri.etsi.org/01903/v1.3.2#"


class Methods(Enum):
    digest = "http://www.w3.org/2000/09/xmldsig#sha1"
    signature = "http://www.w3.org/2000/09/xmldsig#rsa-sha1"
    canonicalization = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    signature_construction = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
