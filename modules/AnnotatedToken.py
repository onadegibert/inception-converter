class AnnotatedToken:

    def __init__(self, token, sentence, tags, text_string, tag_id):
        self.token = token
        self.sentence = sentence
        self.tags = tags
        self.text_string = text_string
        self.annotated_string = ' '.join([each_tag.string for each_tag in self.tags])
        self.tag_id = tag_id
        self.annotation, self.last_tag_id = self.get_annotated_token()

    def get_annotated_token(self):
        tag_id = self.get_id(self.token)
        onset_offset = str(self.token.onset) + "-" + str(self.token.offset)
        if self.token.string in self.annotated_string and self.token.string != '':
            level_1, level_2 = self.matching_tag()
            level_2_tag_id = self.tag_id + 1
            if level_1 != "_":
                level_1 = level_1 + "[" + str(self.tag_id) + "]"
                level_2 = level_2 + "[" + str(level_2_tag_id) + "]"
                last_tag_id = self.tag_id + 2
                return [tag_id, onset_offset, self.token.string,
                        "|".join(["*[" + str(self.tag_id) + "]", "*[" + str(level_2_tag_id) + "]"]),
                        "|".join([level_1, level_2])], last_tag_id
            else:
                return [tag_id, onset_offset, self.token.string, "_", "_"], self.tag_id
        else:
            return [tag_id, onset_offset, self.token.string, "_", "_"], self.tag_id

    def get_id(self, token):
        tag_id = str(self.sentence.sen_id) + "-" + str(self.sentence.tokens.index(token))
        return tag_id

    def matching_tag(self):
        current_tag = "_", "_"
        for tag in self.tags:
            if tag.onset == self.token.onset:  # beginning
                current_tag = tag.level_1, tag.level_2
            elif tag.offset == self.token.offset:  # end
                current_tag = tag.level_1, tag.level_2
            elif self.token.onset > tag.onset and self.token.offset < tag.offset:  # in the middle
                current_tag = tag.level_1, tag.level_2
        return current_tag
