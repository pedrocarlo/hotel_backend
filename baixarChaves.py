import datetime
import os
import shutil
from lxml import etree
from pynfe.utils.flags import NAMESPACE_NFE

# TODO mudar date.month. Tirar isso quando sistema estiver a tona
def escrever_chaves():
    ns = {'ns': NAMESPACE_NFE}
    folder = "../distNfe_xml"
    files = os.listdir(folder)
    chaves = []
    for filename in files:
        with open(folder + "/" + filename, "r") as f:
            xml = f.read()

        resposta = etree.fromstring(xml)
        b_chave = resposta.xpath('//ns:chNFe', namespaces=ns)[0].text
        date = datetime.datetime.fromisoformat(resposta.xpath('//ns:dhEmi', namespaces=ns)[0].text)
        if date.month == 6:
            # print(date)
            chaves.append(b_chave)
        # print(b_chave)
    with open("manifestar.txt", "w") as f:
        f.writelines(chave + '\n' for chave in chaves)


def ler_chaves():
    chaves = []
    with open("manifestar.txt", "r") as f:
        for line in f.readlines():
            chaves.append(line.strip())
    return chaves
