from .Sentence import Sentence
import re


class TsvFile:
    def __init__(self, data, text_string):
        self.data = data
        self.text_string = text_string
        self.sentences = self.parse_data()

    def parse_data(self):
        orig_sentences = self.data
        sentences = list()
        onset_start = 0
        # TODO improve sentence splitting
        for sentence in orig_sentences:
            if sentence != '\n':
                # re.split(':|,| |\.(?!com)'
                sentence = Sentence(sentence, orig_sentences.index(sentence),
                                    re.findall(r"[\w']+|[!\"\[\]#$%&'()*+,-./:;<=>?@^_`{|}~]", sentence), self.text_string,
                                    onset_start)
                onset_start = sentence.onset_start
                sentences.append(sentence)
        return sentences
