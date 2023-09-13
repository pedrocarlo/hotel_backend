from datetime import datetime
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from db.model import Nfe


ns = {"ns": NAMESPACE_NFE}


def get_tags(filepath=None, xml_str=None):
    if xml_str:
        xml = xml_str
    elif filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            xml = f.read()

    resposta = etree.fromstring(xml)
    resumida: bool = True if resposta.xpath("//ns:resNFe", namespaces=ns) else False
    completa: bool = True if resposta.xpath("//ns:nfeProc", namespaces=ns) else False

    if completa or resumida:
        chave: str = resposta.xpath("//ns:chNFe", namespaces=ns)[0].text
        try:
            cnpj_comprador: str = resposta.xpath("//ns:CNPJ", namespaces=ns)[1].text
        except:
            cnpj_comprador: str = None
        cnpj: str = resposta.xpath("//ns:CNPJ", namespaces=ns)[0].text
        nome: str = resposta.xpath("//ns:xNome", namespaces=ns)[0].text.upper()
        total = float(resposta.xpath("//ns:vNF", namespaces=ns)[0].text)
        date: datetime = datetime.fromisoformat(
            resposta.xpath("//ns:dhEmi", namespaces=ns)[0].text
        )
        irrelevant: bool = False
        manifestada: bool = completa

        nota = Nfe(
            chave,
            cnpj_comprador,
            cnpj,
            nome,
            total,
            date,
            completa,
            manifestada=manifestada,
            irrelevant=irrelevant,
        )
        return nota
    else:
        return None
