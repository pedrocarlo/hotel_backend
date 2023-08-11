import datetime

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from utils import Certificado
from baixarChaves import ler_chaves
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
    if codigo_ret < CODIGO_PROCESSADO:
        if codigo_ret >= CODIGO_SUCESSO:
            print("CODIGO RETORNO")
            print(codigo_ret)
            download_xml(resposta)
            if is_nsu:
                ultNsu = int(resposta.xpath("//ns:ultNSU", namespaces=ns)[0].text)
                maxNsu = int(resposta.xpath("//ns:maxNSU", namespaces=ns)[0].text)

                print("UltNSU ", ultNsu)
                print("Max NSU", maxNsu)
                return ultNsu, maxNsu

    return 0, 0


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
            des_resposta, tipo = filter_xml(des_resposta)
            # print(b_chave)
            if tipos["evento"] == tipo:
                des_resposta.getroottree().write(
                    f"eventos/{b_chave}.xml", pretty_print=True
                )
            if tipos["nfe"] == tipo:
                des_resposta.getroottree().write(
                    f"distNfe_xml/{b_chave}.xml", pretty_print=True
                )
            if tipos["cancelamento"] == tipo:
                des_resposta.getroottree().write(
                    f"cancelados/{b_chave}.xml", pretty_print=True
                )
    except Exception as e:
        print("Programa executou mas teve o seguinte erro Handled:")
        print(e)
        print(etree.tostring(curr_res.getroottree(), pretty_print=True))
        traceback.print_exc()
        curr_res.getroottree().write(f"errors/{b_chave}.xml", pretty_print=True)


distNfe(CHAVE, NSU, False, False)

nsu = 0
# maxNsu = float("inf")
# while nsu <= maxNsu != 0:
#     nsu, maxNsu = distNfe("", nsu, True, False)
# distNfe(CHAVE, NSU, is_nsu=False, is_nsu_especifico=True)
