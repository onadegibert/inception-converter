class TsvAnnotation:
    def __init__(self, sentence, tags, text_string, tag_id):
        self.sentence = sentence
        self.tags = tags
        self.text_string = text_string
        self.tag_id = tag_id
        self.annotation, self.last_tag_id = self.get_tag()

    def get_tag(self):
        annotated_sentence = list()
        last_entity = ""
        last_annotation = ""
        last_tag_id = self.tag_id
        for each_token in self.sentence.tokens:
            annotated_token = AnnotatedToken(each_token, self.sentence, self.tags, self.text_string, self.tag_id)
            if annotated_token.annotation[4].split("[")[0] == last_entity: # if the last entity is the same
                if last_entity != "_":
                    annotated_token.annotation[3] = last_annotation[0]
                    annotated_token.annotation[4] = last_annotation[1]
                    last_tag_id = annotated_token.last_tag_id - 2
            else:
                last_tag_id = annotated_token.last_tag_id
            self.tag_id = last_tag_id
            last_entity = annotated_token.annotation[4].split("[")[0]
            #TODO compare if the second entity is the same
            last_annotation = [annotated_token.annotation[3],annotated_token.annotation[4]]
            annotated_sentence.append(annotated_token.annotation)
        return annotated_sentence, last_tag_id


class AnnotatedToken:

    def __init__(self, token, sentence, tags, text_string, tag_id):
        self.token = token
        self.sentence = sentence
        self.tags = tags
        self.text_string = text_string
        self.annotated_string = ' '.join([each_tag.string for each_tag in self.tags])
        self.tag_id = tag_id
        self.annotation, self.last_tag_id = self.get_annotated_token(tag_id)

    def get_annotated_token(self, tag_id):
        id = self.get_id(self.token)
        onset_offset = str(self.token.onset) + "-" + str(self.token.offset)
        if self.token.string in self.annotated_string and self.token.string != '':
            level_1, level_2 = self.matching_tag()
            level_2_tag_id = self.tag_id + 1
            # TODO create annotation class
            if level_1 != "_":
                level_1 = level_1 + "[" + str(self.tag_id) + "]"
                level_2 = level_2 + "[" + str(level_2_tag_id) + "]"
                last_tag_id = self.tag_id + 2
                return [id, onset_offset, self.token.string,
                        "|".join(["*[" + str(self.tag_id) + "]", "*[" + str(level_2_tag_id) + "]"]),
                        "|".join([level_1, level_2])], last_tag_id
            else:
                return [id, onset_offset, self.token.string, "_", "_"], self.tag_id
        else:
            return [id, onset_offset, self.token.string, "_", "_"], self.tag_id

    def get_id(self, token):
        id = str(self.sentence.sen_id) + "-" + str(self.sentence.tokens.index(token))
        return id

    def matching_tag(self):
        current_tag = "_", "_"
        # TODO use tag.id
        for tag in self.tags:
            if tag.onset == self.token.onset:  # beggining
                current_tag = tag.level_1, tag.level_2
            elif tag.offset == self.token.offset:  # end
                current_tag = tag.level_1, tag.level_2
            elif self.token.onset > tag.onset and self.token.offset < tag.offset:  # in the middle
                current_tag = tag.level_1, tag.level_2
        return current_tag
