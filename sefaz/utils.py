from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE


class Certificado:
    # certificado = "C:\\Users\\Pedro Muniz\\Documents\\Certificados\\LIBLANCO_EMPREENDIMENTOS_IMOBILIARIOS_LTDA_51548782000139.pfx"
    # certificado = "/Users/mariamuniz/Development/LIBLANCO EMPREENDIMENTOS IMOBILIARIOS LTDA_51548782000139.pfx"
    # TODO trocar isso aqui
    certificado = '../certificado/certificado.pfx'
    senha = "548782"
    uf = "sp"
    homologacao = False
    cnpj = "51548782000139"
