from AnnotatedFile import AnnotatedFile
from WebAnnoObject import WebAnnoObject

filename = '../output/ona/MAPA_S0004-06142005000500011-1.xml'


def test_open_file():
    file = AnnotatedFile(filename)
    assert file

def test_web_anno():
    file = AnnotatedFile(filename)
    file_object = WebAnnoObject(file)
    assert file_object
