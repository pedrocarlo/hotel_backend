from datetime import datetime
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from db.model import Nfe


ns = {"ns": NAMESPACE_NFE}


def get_tags(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        xml = f.read()

    resposta = etree.fromstring(xml)

    chave: str = resposta.xpath("//ns:chNFe", namespaces=ns)[0].text
    cnpj: str = resposta.xpath("//ns:CNPJ", namespaces=ns)[0].text
    nome: str = resposta.xpath("//ns:xNome", namespaces=ns)[0].text
    total = float(resposta.xpath("//ns:vNF", namespaces=ns)[0].text)
    date: datetime = datetime.fromisoformat(
        resposta.xpath("//ns:dhEmi", namespaces=ns)[0].text
    )
    resumida: bool = True if resposta.xpath("//ns:resNFe", namespaces=ns) else False
    completa: bool = (
        True if resposta.xpath("//ns:procEventoNFe", namespaces=ns) else False
    )

    nota = Nfe(chave, cnpj, nome, total, date, completa)
    return nota
