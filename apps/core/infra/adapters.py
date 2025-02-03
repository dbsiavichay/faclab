from typing import List

import requests

from apps.core.domain.entities import UploadFile
from apps.core.domain.ports import SealifyPort


class BaseHttpClient:
    DEFAULT_HEADERS = {"Accept": "application/json"}

    def get_headers(self, headers):
        return {**self.DEFAULT_HEADERS, **headers}

    def get(self, *args, headers={}, **kwargs):
        response = requests.get(*args, headers=self.get_headers(headers), **kwargs)
        response.raise_for_status()

        return response

    def post(self, *args, headers={}, **kwargs):
        response = requests.post(*args, headers=self.get_headers(headers), **kwargs)
        response.raise_for_status()

        return response

    def delete(self, *args, headers={}, **kwargs):
        response = requests.delete(*args, headers=self.get_headers(headers), **kwargs)
        response.raise_for_status()

        return response


class SealifyAdapter(SealifyPort, BaseHttpClient):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_certificate(self, certificate: UploadFile, password: str) -> dict:
        url = f"{self.base_url}/api/certificates"

        files = {
            "certificate": (
                certificate.filename,
                certificate.file,
                certificate.content_type,
            )
        }
        response = self.post(url, files=files, data={"password": password})
        return response.json()

    def list_certificates(self) -> List[dict]:
        url = f"{self.base_url}/api/certificates"
        response = self.get(url)
        return response.json()

    def delete_certificate(self, certificate_id: str) -> None:
        url = f"{self.base_url}/api/certificates/{certificate_id}"
        self.delete(url)

    def seal_invoice(self, invoice_xml: str, certificate_id: str) -> dict:
        url = f"{self.base_url}/api/certificates/{certificate_id}/seal-invoice"
        response = self.post(url, json={"invoiceXML": invoice_xml})
        return response.json()
