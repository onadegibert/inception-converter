from .Token import Token


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
