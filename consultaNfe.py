from pynfe.processamento.comunicacao import ComunicacaoSefaz
from lxml import etree
from pynfe.utils.flags import NAMESPACE_NFE

certificado = "C:\\Users\\Pedro Muniz\\Documents\\Certificados\\LIBLANCO_EMPREENDIMENTOS_IMOBILIARIOS_LTDA_51548782000139.pfx"
senha = '548782'
uf = 'sp'
homologacao = False

chave_acesso = '35230622712006000124550010001086721765458230'
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.consulta_nota('nfe', chave_acesso)  # nfe ou nfce
print(envio.content)  # SEFAZ SP utilizar envio.content

ns = {'ns': NAMESPACE_NFE}
prot = etree.fromstring(envio.text.encode('utf-8'))  # SEFAZ SP utilizar envio.content
status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
if status == '100':
    prot_nfe = prot[0][0].xpath('ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
    xml = etree.tostring(prot_nfe, encoding='unicode')
    print(xml)
