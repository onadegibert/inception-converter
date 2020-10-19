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
        #TODO improve sentence splitting
        for sentence in orig_sentences:
            #re.split(':|,| |\.(?!com)'
            sentence = Sentence(sentence, orig_sentences.index(sentence), re.findall(r"[\w']+|[!\"\[\]#$%&'()*+,-./:;<=>?@\^_`{|}~]", sentence), self.text_string, onset_start)
            onset_start = sentence.onset_start
            #sentence = Sentence(sentence, orig_sentences.index(sentence), sentence.split(), self.text_string)
            sentences.append(sentence)
        return sentences


class Sentence:
    def __init__(self, sentence, sen_id, tokens, text_string, onset_start):
        self.string = ''.join(sentence)
        self.sen_id = sen_id
        self.tokens = tokens
        self.text_string = text_string
        self.onset_start = onset_start
        self.tokens = self.parse_tokens()

    def parse_tokens(self):
        parsed_tokens = list()
        for each_token in self.tokens:
            each_token = Token(each_token, self.text_string, self.onset_start)
            self.onset_start = each_token.offset
            parsed_tokens.append(each_token)
        return parsed_tokens


class Token:
    def __init__(self, string, text_string, onset_start):
        self.string = string
        self.text_string = text_string
        self.onset_start = onset_start
        self.onset, self.offset = self.onset_offset()

    def onset_offset(self):
        onset = self.text_string.find(self.string, self.onset_start)
        offset = onset + len(self.string)
        return onset, offset
