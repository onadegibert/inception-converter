from .AnnotatedToken import AnnotatedToken
from .Annotation import Annotation
import re


class TsvAnnotation:
    def __init__(self, sentence, tags, text_string, tag_id):
        self.sentence = sentence
        self.tags = tags
        self.text_string = text_string
        self.tag_id = tag_id
        self.annotation, self.last_tag_id = self.get_tag()

    def get_tag(self):
        annotated_sentence = list()
        last_entity_1 = ""
        last_entity_2 = ""
        last_annotation_tag_1 = ""
        last_annotation_entity_1 = ""
        last_annotation_tags = ""
        last_annotation_entities = ""
        last_tag_id = self.tag_id
        for each_token in self.sentence.tokens:
            annotated_token = AnnotatedToken(each_token, self.sentence, self.tags, self.text_string, self.tag_id)
            annotation_info = Annotation(re.split(r"]|\||\[", annotated_token.annotation[4]))
            last_tag_id = get_token_tags(annotated_token, annotation_info, last_annotation_entities,
                                         last_annotation_entity_1, last_annotation_tag_1, last_annotation_tags,
                                         last_entity_1, last_entity_2)
            self.tag_id = last_tag_id
            last_entity_1 = annotation_info.level_1_entity
            last_entity_2 = annotation_info.level_2_entity
            last_annotation_tags = annotated_token.annotation[3]
            last_annotation_entities = annotated_token.annotation[4]
            if last_entity_1 != "_":
                if len(annotated_token.annotation[3].split("|")) > 1:
                    last_annotation_tag_1, last_annotation_tag_2 = annotated_token.annotation[3].split("|")
                    last_annotation_entity_1, last_annotation_entity_2 = annotated_token.annotation[4].split("|")
                else:
                    last_annotation_tag_1, last_annotation_tag_2 = annotated_token.annotation[3], ''
                    last_annotation_entity_1, last_annotation_entity_2 = annotated_token.annotation[4], ''
            annotated_sentence.append(annotated_token.annotation)
        return annotated_sentence, last_tag_id


def get_token_tags(annotated_token, annotation_info, last_annotation_entities, last_annotation_entity_1,
                   last_annotation_tag_1, last_annotation_tags, last_entity_1, last_entity_2):
    # Drop none tags at level_1 and level_2
    if annotation_info.level_1_entity == "none":
        annotated_token.annotation[3] = "*[" + annotation_info.level_1_tag + "]"
        annotated_token.annotation[4] = annotation_info.level_2_entity + annotated_token.annotation[3].replace("*",
                                                                                                               "")
        last_tag_id = int(annotation_info.level_2_tag)
        annotated_token.last_tag_id = last_tag_id
    elif annotation_info.level_2_entity == "none":
        annotated_token.annotation[3] = "*[" + annotation_info.level_1_tag + "]"
        annotated_token.annotation[4] = annotation_info.level_1_entity + annotated_token.annotation[3].replace("*",
                                                                                                               "")
        last_tag_id = int(annotation_info.level_2_tag)
        annotated_token.last_tag_id = last_tag_id
    if last_entity_1 != "_":
        if annotation_info.level_1_entity == last_entity_1:  # if the last entity 1 is the same
            if annotation_info.level_2_entity == last_entity_2:  # if the last entity 2 is the same
                annotated_token.annotation[3] = last_annotation_tags
                annotated_token.annotation[4] = last_annotation_entities
                if annotation_info.level_2_entity == "none" or annotation_info.level_1_entity == "none":
                    last_tag_id = annotated_token.last_tag_id - 1
                else:
                    last_tag_id = annotated_token.last_tag_id - 2
            else:
                if annotation_info.level_2_entity == "none":  # Cases of stopwords within dates such as "5 de
                    # Noviembre de 2020"
                    annotated_token.annotation[3] = "*[" + str(int(annotation_info.level_1_tag) - 2) + "]"
                    annotated_token.annotation[4] = annotation_info.level_1_entity + annotated_token.annotation[
                        3].replace("*", "")
                    last_tag_id = int(annotation_info.level_1_tag)
                    annotated_token.last_tag_id = last_tag_id
                else:
                    annotated_token.annotation[3] = last_annotation_tag_1 + "|*[" + str(
                        annotated_token.last_tag_id - 2) + "]"
                    annotated_token.annotation[
                        4] = last_annotation_entity_1 + "|" + annotation_info.level_2_entity + "[" + str(
                        annotated_token.last_tag_id - 2) + "]"
                    last_tag_id = (annotated_token.last_tag_id - 1)
        else:
            last_tag_id = annotated_token.last_tag_id
    else:
        last_tag_id = annotated_token.last_tag_id
    return last_tag_id
