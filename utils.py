from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree


class Certificado:
    certificado = "C:\\Users\\Pedro Muniz\\Documents\\Certificados\\LIBLANCO_EMPREENDIMENTOS_IMOBILIARIOS_LTDA_51548782000139.pfx"
    senha = '548782'
    uf = 'sp'
    homologacao = False
    CNPJ = "51548782000139"
