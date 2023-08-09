from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoManifestacaoDest
from pynfe.entidades.fonte_dados import _fonte_dados
import datetime

from pynfe.utils.flags import NAMESPACE_NFE

from sefaz.baixarChaves import escrever_chaves, ler_chaves
from sefaz.utils import Certificado

certificado = Certificado.certificado
senha = Certificado.senha
uf = Certificado.uf
homologacao = Certificado.homologacao

chaves = ler_chaves()

CNPJ = '51548782000139'
CHAVE = chaves[0]


def manifestNfe(chave: str, CNPJ: str):
    ns = {'ns': NAMESPACE_NFE}
    CODIGO_SUCESSO = 128
    ciencia_emissao = 2
    ciencia_operacao = 1
    manif_dest = EventoManifestacaoDest(
        cnpj=CNPJ,  # cnpj do destinatário
        chave=chave,  # chave de acesso da nota
        data_emissao=datetime.datetime.now(),
        uf='AN',
        operacao=ciencia_operacao  # - numero da operacao
    )
    # serialização
    serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
    nfe_manif = serializador.serializar_evento(manif_dest)
    # assinatura
    a1 = AssinaturaA1(certificado, senha)
    xml = a1.assinar(nfe_manif)
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    envio = con.evento(modelo='nfe', evento=xml)  # modelo='nfce' ou 'nfe'
    print(envio.text)
    motivos = envio.xpath('//ns:xMotivo', namespaces=ns)
    codigo_rets = envio.xpath('//ns:cStat', namespaces=ns)
    motivo_processamento = motivos[0].text
    codigo_ret_processamento = int(codigo_rets[0].text)
    print(motivo_processamento)
    print(codigo_ret_processamento)

    motivo = motivos[1].text
    codigo_ret = int(codigo_rets[1].text)
    print(motivo)
    print(codigo_ret)
    if codigo_ret <= CODIGO_SUCESSO:
        pass
        # adicione em outra pasta o arquivo e update banco de dados


# for chave in chaves[20:40]:
#     manifestNfe(chave, CNPJ)
