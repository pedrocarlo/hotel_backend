import re

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from utils import Certificado
from sefaz.baixarChaves import escrever_chaves, ler_chaves
import traceback

chaves = ler_chaves()

# CHAVE = '35230732165635000135550020000875431000954920'  # deixar a chave de acesso vazia
CHAVE = chaves[0]
NSU = 4181  # baixar o xml do NSU especifico
maxNsu = float('inf')

count = 121
ns = {'ns': NAMESPACE_NFE}


def distNfe(chave, nsu, is_nsu: bool, is_nsu_especifico: bool):
    maxNsu = float('inf')

    CODIGO_PROCESSADO = 200
    CODIGO_SUCESSO = 137
    CNPJ = Certificado.CNPJ

    certificado = Certificado.certificado
    senha = Certificado.senha
    uf = Certificado.uf
    homologacao = Certificado.homologacao

    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    if is_nsu:
        if is_nsu_especifico:
            xml = con.consulta_distribuicao(cnpj=CNPJ, chave='', nsu=nsu, consulta_nsu_especifico=True)
        else:
            xml = con.consulta_distribuicao(cnpj=CNPJ, chave='', nsu=nsu, consulta_nsu_especifico=False)
    else:
        xml = con.consulta_distribuicao(cnpj=CNPJ, chave=chave)

    print(xml.content)

    resposta = etree.fromstring(xml.content)

    motivo = resposta.xpath('//ns:xMotivo', namespaces=ns)[0].text
    print(motivo)
    codigo_ret = int(resposta.xpath('//ns:cStat', namespaces=ns)[0].text)
    print(codigo_ret)
    if codigo_ret < CODIGO_PROCESSADO:
        if codigo_ret >= CODIGO_SUCESSO:
            download_xml(resposta)
            if is_nsu:
                ultNsu = int(resposta.xpath('//ns:ultNSU', namespaces=ns)[0].text)
                maxNsu = int(resposta.xpath('//ns:maxNSU', namespaces=ns)[0].text)

                print("UltNSU ", ultNsu)
                print("Max NSU", maxNsu)
                return ultNsu, maxNsu

    return 0, 0


def download_xml(resposta):
    curr_res = None
    try:
        zip_respostas = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)
        print(zip_respostas)

        for zip_res in zip_respostas:
            des_resposta = DescompactaGzip.descompacta(zip_res.text)
            curr_res = des_resposta
            b_chave = des_resposta.xpath('//ns:chNFe', namespaces=ns)[0].text
            date = des_resposta.xpath('//ns:dhEmi', namespaces=ns)[0].text
            print(date)
            print(b_chave)

            des_resposta.getroottree().write(f'../distNfe_xml/{b_chave}.xml', pretty_print=True)

    except IndexError as e:
        print('Programa executou mas teve o seguinte erro Handled')
        traceback.print_exc()
        print(etree.tostring(curr_res.getroottree(), pretty_print=True))
        curr_res.getroottree().write(f'../error.xml', pretty_print=True)


# while NSU < maxNsu + 1 and NSU < NSU + 20:
#     distNfe()
#
#     count += 1
#     NSU = NSU + 1
#     print('NSU ', NSU)

for chave in chaves[:20]:
    distNfe(chave, NSU, False, False)
# nsu = 0
# maxNsu = float("inf")
# while nsu <= maxNsu != 0:
#     nsu, maxNsu = distNfe("", nsu, True, False)




