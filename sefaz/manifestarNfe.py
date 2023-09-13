from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoManifestacaoDest
from pynfe.entidades.fonte_dados import _fonte_dados
import datetime

from pynfe.utils.flags import NAMESPACE_NFE
from db.sql import get_by_date, get_session

from sefaz.baixarChaves import escrever_chaves, ler_chaves
from sefaz.utils import get_certificados


certificados = get_certificados()
# CNPJ = "51548782000139"
# CHAVE = chaves[0]


def manifestNfe(chave: str, tipo: int = 1, Certificado=certificados[0]):
    certificado = Certificado.certificado
    senha = Certificado.senha
    uf = Certificado.uf
    homologacao = Certificado.homologacao
    CNPJ = Certificado.cnpj

    manif_dest = EventoManifestacaoDest(
        cnpj=CNPJ,  # cnpj do destinatário
        chave=chave,  # chave de acesso da nota
        data_emissao=datetime.datetime.now(),
        uf="AN",
        operacao=tipo,  # - numero da operacao
    )
    # serialização
    serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
    nfe_manif = serializador.serializar_evento(manif_dest)
    # assinatura
    a1 = AssinaturaA1(certificado, senha)
    xml = a1.assinar(nfe_manif)
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    envio = con.evento(modelo="nfe", evento=xml)  # modelo='nfce' ou 'nfe'
    print(envio.text)


# manifestNfe("35230871998819000138550010000022771002245280", CNPJ=CNPJ)
