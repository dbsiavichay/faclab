import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.models import model_to_dict

from apps.sites.domain.enums import Emissions, Environments
from apps.sites.infra.forms import ConfigForm, SignatureForm
from apps.sites.models import Config, Signature


class TestSignatureForm:
    @pytest.mark.django_db
    def test_signature_create(self, signature_file_p12):
        p12_bytes, password, metadata = signature_file_p12
        p12 = SimpleUploadedFile(
            "test.p12", p12_bytes, content_type="application/x-pkcs12"
        )
        data = {"signature_password": password}
        files = {"signature_file": p12}
        form = SignatureForm(data, files)

        assert form.is_valid() is True
        assert not form.errors

        signature = form.save()

        assert isinstance(signature, Signature)
        assert metadata == model_to_dict(signature, fields=metadata.keys())

    def test_signature_create_invalid(self):
        p12 = SimpleUploadedFile("test.mp4", b"contect", content_type="video/mp4")
        data = {"signature_password": "test"}
        files = {"signature_file": p12}
        form = SignatureForm(data, files)

        assert form.is_valid() is False
        assert form.errors


class TestConfigForm:
    @pytest.mark.django_db
    def test_config_create(self):
        data = {
            "code": "1460000290001",
            "company_name": "test",
            "company_trade_name": "test",
            "main_address": "test",
            "company_address": "test",
            "company_code": "test",
            "company_point_sale_code": "test",
            "special_taxpayer_resolution": "test",
            "withholding_agent_resolution": "test",
            "accounting_required": False,
            "environment": str(Environments.TESTING),
            "emission": str(Emissions.NORMAL),
            "iva_percent": 12,
            "signature": None,
        }
        form = ConfigForm(data)

        assert form.is_valid() is True
        assert not form.errors

        config = form.save()

        assert isinstance(config, Config)
        assert data == model_to_dict(config, fields=("sri_config",)).get("sri_config")

    def test_config_create_invalid(self):
        data = {}
        form = ConfigForm(data)

        assert form.is_valid() is False
        assert form.errors
