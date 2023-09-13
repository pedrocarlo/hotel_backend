import sys, inspect
import types


# class Certificado:
#     # certificado = "C:\\Users\\Pedro Muniz\\Documents\\Certificados\\LIBLANCO_EMPREENDIMENTOS_IMOBILIARIOS_LTDA_51548782000139.pfx"
#     # certificado = "/Users/mariamuniz/Development/LIBLANCO EMPREENDIMENTOS IMOBILIARIOS LTDA_51548782000139.pfx"
#     # TODO trocar isso aqui
#     certificado = "./certificado/51548782000139.pfx"
#     senha = "548782"
#     uf = "sp"
#     homologacao = False
#     cnpj = "51548782000139"

# def get_certificados(self):
#     folder = "./certificado"
#     import os

#     return os.listdir(folder)


class LiblancoCert:
    certificado = "./certificado/51548782000139.pfx"
    senha = "548782"
    uf = "sp"
    homologacao = False
    cnpj = "51548782000139"


class CondominioCert:
    certificado = "./certificado/67149070000187.pfx"
    senha = "67149070"
    uf = "sp"
    homologacao = False
    cnpj = "67149070000187"


def get_certificados() -> list:
    certificados = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for cert in classes:
        certificados.append(cert[1])
    return certificados
