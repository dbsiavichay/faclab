import base64
import os

import requests
from django.conf import settings
from suds.client import Client


class SRIClient:
    TEST_ENVIRONMENT = 1
    PRODUCTION_ENVIRONMENT = 2

    SRI_URL = "https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"
    SRI_RUC_URL = "https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/Persona/obtenerPersonaDesdeRucPorIdentificacion?numeroRuc=%s"

    RETENTION_SEND_WS = {
        TEST_ENVIRONMENT: "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl",
        PRODUCTION_ENVIRONMENT: "",
    }
    RETENTION_FETCH_WS = {
        TEST_ENVIRONMENT: "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"
    }

    def __init__(self):
        try:
            self.client = Client(
                "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"
            )
        except Exception as e:
            raise Exception("Problemas de red al conectarse con el SRI " + str(e))

    def send_voucher(self, path):
        try:
            with open(path, "rb") as file:
                data = base64.encodebytes(file.read()).decode("utf-8")
                result = self.client.service.validarComprobante(data)

            file.close()
        except Exception as e:
            raise Exception("Problemas al enviar la rentención al SRI " + str(e))

        if result.estado == "DEVUELTA":
            messages = [
                mensaje.mensaje.capitalize()
                for mensaje in result.comprobantes.comprobante[0].mensajes.mensaje
            ]
            message = "Devuelta por el SRI: " + " * ".join(messages)
            raise Exception(message)

    @classmethod
    def fetch_retention(cls, code):
        client = cls.get_client(cls.RETENTION_FETCH_WS)
        try:
            result = client.service.autorizacionComprobante(code)
        except Exception as e:
            raise Exception("Problemas traer la retención del SRI " + str(e))
        if hasattr(result, "numeroComprobantes"):
            number_of_vouchers = int(result.numeroComprobantes)
            if not number_of_vouchers:
                raise Exception("La clave de acceso consultada es incorrecta")
        if result.autorizaciones.autorizacion[0].estado == "NO AUTORIZADO":
            messages = [
                mensaje.mensaje.capitalize()
                for mensaje in result.autorizaciones.autorizacion[0].mensajes.mensaje
            ]
            message = "Devuelta por el SRI: " + " * ".join(messages)
            raise Exception(message)

        return result.autorizaciones.autorizacion[0].comprobante

    @classmethod
    def fetch_taxpayer(cls, code):
        URL = cls.SRI_RUC_URL % code
        response = requests.get(URL)
        data = response.json()
        names = data.get("nombreCompleto").split()
        first_name = " ".join(names[-2:])
        last_name = names[0] if len(names) == 3 else " ".join(names[:2])
        taxpayer = {
            "code": data.get("identificacion"),
            "fullname": data.get("nombreCompleto"),
            "first_name": first_name,
            "last_name": last_name,
            "type": data.get("tipoPersona"),
        }
        return taxpayer


EXCEPTIONS = {
    "java.io.FileNotFoundException": "FileNotFoundException",
    "java.security.KeyStoreException": "WrongPasswordException",
    "io.rubrica.exceptions.HoraServidorException": "NetworkException",
    "RevokedException": "ExpiredCertificateException",
    "ExpiredException": "ExpiredCertificateException",
    "io.rubrica.exceptions.CertificadoInvalidoException": "InvalidCertificateException",
    "java.lang.IllegalArgumentException": "IllegalArgumentException",
    "java.lang.NumberFormatException": "NumberFormatException",
    "java.lang.ArrayIndexOutOfBoundsException": "ArrayArgumentException",
}


class BaseSigner:
    PATH_BASE = str(settings.BASE_DIR / "apps/sri/libs")
    CLASSPATH = f".:{PATH_BASE}:"
    JAR_PATH = f"{PATH_BASE}/Rubrica-jar-with-dependencies.jar:"

    def __init__(self, certificate, password):
        self.cert_chain = certificate
        self.password = password

        java_class = "Validate"
        command = f"java -cp {self.CLASSPATH}{self.JAR_PATH} {java_class} {self.cert_chain} {self.password}"
        result = os.popen(command).read()

        for key, value in EXCEPTIONS.items():
            if key in result:
                raise Exception(value)


class XMLSigner(BaseSigner):
    XML_JAR_PATH = f"{BaseSigner.PATH_BASE}/SRISigner.jar"

    def sign(self, xml_path):
        out_path = "/".join(xml_path.split("/")[0:-1])
        out_file_name = xml_path.split("/")[-1]
        """
        command = [
            "java", "-jar", cls.JAR_PATH,
            xml_path, cls.SIGN_PATH, cls.SIGN_PASSWORD,
            out_path, out_file_name,
        ]
        """
        command = f"java -jar {self.XML_JAR_PATH} {xml_path} {self.cert_chain} {self.password} {out_path} {out_file_name}"
        try:
            result = os.popen(command).read()
        except ValueError as e:
            raise Exception(str(e))
