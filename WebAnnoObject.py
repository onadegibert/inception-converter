from TsvFile import TsvFile
from TsvAnnotation import TsvAnnotation


class WebAnnoObject:
    def __init__(self, file_object, tag_id):
        self.file_object = file_object
        self.tag_id = tag_id
        self.tags = file_object.tags
        self.tsv_file = self.process_tsv()

    def process_tsv(self):
        tsv_file = TsvFile(self.file_object.text, self.file_object.text_string)
        initial_text = "#FORMAT=WebAnno TSV 3.2\n#T_SP=de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity|identifier|value\n"
        print(initial_text)
        for each_sen in tsv_file.sentences:
            print("\n#Text="+each_sen.string)
            annotated_sentence = TsvAnnotation(each_sen, self.tags, self.file_object.text_string, self.tag_id)
            self.tag_id = annotated_sentence.last_tag_id
            for each_annotation in annotated_sentence.annotation:
                print('\t'.join(each_annotation))
            #TODO fix tag_id obtention method
            #tag_id += 2
        return tsv_file
