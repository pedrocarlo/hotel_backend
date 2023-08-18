import datetime

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from sefaz.utils import Certificado
from sefaz.baixarChaves import ler_chaves
from sefaz.xml_parser import get_tags
import traceback

chaves = ler_chaves()

CNPJ = "51548782000139"
# CHAVE = '35230732165635000135550020000875431000954920'  # deixar a chave de acesso vazia
CHAVE = "35230655721559000100550030030706761542551284"
CHAVE = chaves[0]
NSU = 4131  # baixar o xml do NSU especifico
maxNsu = float("inf")

count = 121
ns = {"ns": NAMESPACE_NFE}

tipos = {
    "nfe": 0,
    "evento": 1,
    "cancelamento": 2,
}

NFE = 0
EVENTO = 1
CANCELAMENTO = 2


def distNfe(chave, nsu, is_nsu: bool, is_nsu_especifico: bool):
    maxNsu = float("inf")
    CODIGO_PROCESSADO = 200
    CODIGO_SUCESSO = 137
    # CNPJ = '51548782000139'
    CNPJ = Certificado.cnpj
    certificado = Certificado.certificado
    senha = Certificado.senha
    uf = Certificado.uf
    homologacao = Certificado.homologacao

    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    if is_nsu:
        if is_nsu_especifico:
            xml = con.consulta_distribuicao(
                cnpj=CNPJ, chave="", nsu=nsu, consulta_nsu_especifico=True
            )
        else:
            xml = con.consulta_distribuicao(
                cnpj=CNPJ, chave="", nsu=nsu, consulta_nsu_especifico=False
            )
    else:
        xml = con.consulta_distribuicao(cnpj=CNPJ, chave=chave)

    # print(xml.content)

    resposta = etree.fromstring(xml.content)

    motivo = resposta.xpath("//ns:xMotivo", namespaces=ns)[0].text
    print(motivo)
    codigo_ret = int(resposta.xpath("//ns:cStat", namespaces=ns)[0].text)
    print(codigo_ret)
    xmls = []
    if codigo_ret < CODIGO_PROCESSADO:
        if codigo_ret >= CODIGO_SUCESSO:
            print("CODIGO RETORNO")
            print(codigo_ret)
            xmls = download_xml(resposta)
            if is_nsu:
                ultNsu = int(resposta.xpath("//ns:ultNSU", namespaces=ns)[0].text)
                maxNsu = int(resposta.xpath("//ns:maxNSU", namespaces=ns)[0].text)

                print("UltNSU ", ultNsu)
                print("Max NSU", maxNsu)
                return ultNsu, maxNsu, xmls
            
    return 0, 0, codigo_ret, xmls


def filter_xml(initial_resposta):
    res_cancelamento = initial_resposta.xpath("//ns:procEventoNFe", namespaces=ns)
    res_evento = initial_resposta.xpath("//ns:resEvento", namespaces=ns)
    res_nfe = initial_resposta.xpath("//ns:resNFe", namespaces=ns)

    if res_cancelamento:
        return res_cancelamento[0], tipos["cancelamento"]
    if res_evento:
        return res_evento[0], tipos["evento"]
    if res_nfe:
        return res_nfe[0], tipos["nfe"]


def download_xml(resposta):
    curr_res = None
    xmls = []
    try:
        zip_respostas = resposta.xpath(
            "//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip", namespaces=ns
        )
        # print(zip_respostas)
        
        for zip_res in zip_respostas:
            des_resposta = DescompactaGzip.descompacta(zip_res.text)

            # checar se tem resEvento ou resNfe
            b_chave = des_resposta.xpath("//ns:chNFe", namespaces=ns)[0].text
            curr_res = des_resposta
            xml = etree.tostring(des_resposta.getroottree())
            xmls.append(xml)
            
    except Exception as e:
        print("Programa executou mas teve o seguinte erro Handled:")
        print(e)
        print(etree.tostring(curr_res.getroottree(), pretty_print=True))
        traceback.print_exc()
        curr_res.getroottree().write(f"errors/{b_chave}.xml", pretty_print=True)
    return xmls
chave = "35230624614269000126550010003386141336538648"
# distNfe(CHAVE, NSU, False, False)s

nsu = 0
# maxNsu = float("inf")
# while nsu <= maxNsu != 0:
#     nsu, maxNsu = distNfe("", nsu, True, False)
# distNfe(CHAVE, NSU, is_nsu=False, is_nsu_especifico=True)
