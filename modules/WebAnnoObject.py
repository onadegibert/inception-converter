from modules.TsvFile import TsvFile
from modules.TsvAnnotation import TsvAnnotation


class WebAnnoObject:
    def __init__(self, file_object, tag_id):
        self.file_object = file_object
        self.tag_id = tag_id
        self.tags = file_object.tags
        self.converted_file = self.process_tsv()

    def process_tsv(self):
        final_file = list()
        tsv_file = TsvFile(self.file_object.text, self.file_object.text_string)
        initial_text = ["#FORMAT=WebAnno TSV 3.2","#T_SP=de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity|identifier|value\n"]
        final_file.extend(initial_text)
        for each_sen in tsv_file.sentences:
            final_file.append("\n#Text="+each_sen.string.strip())
            annotated_sentence = TsvAnnotation(each_sen, self.tags, self.file_object.text_string, self.tag_id)
            self.tag_id = annotated_sentence.last_tag_id
            for each_annotation in annotated_sentence.annotation:
                final_file.append('\t'.join(each_annotation))
        return final_file
