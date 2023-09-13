from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from sefaz.utils import get_certificados


def get_validade(certificado=get_certificados()[0]):
    pkcs12 = crypto.load_pkcs12(
        open(certificado.certificado, "rb").read(), certificado.senha.encode("ascii")
    )
    pem_data = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
    cert = x509.load_pem_x509_certificate(pem_data, default_backend())
    return cert.not_valid_after
