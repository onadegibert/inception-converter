from AnnotatedFile import AnnotatedFile
from WebAnnoObject import WebAnnoObject

def main():
    file = AnnotatedFile('../output/ona/MAPA_S0004-06142005000500011-1.xml')
    tsv_file = WebAnnoObject(file, 1)

main()
