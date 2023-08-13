import os
import sefaz.xml_parser as parser
from db.model import Nfe


cwd = os.getcwd()
folder = cwd + "/" + "xml/nfe"
chave_set = set()
for filename in folder:
    filepath = os.path.join(folder, filename)
    nota: Nfe = parser.get_tags()
    if nota.chave not in chave_set:
        pass
