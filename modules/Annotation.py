class Annotation:
    def __init__(self, annotation_info):
        if annotation_info[0] != "_":
            self.level_1_entity = annotation_info[0]
            self.level_2_entity = annotation_info[3]
            self.level_1_tag = annotation_info[1]
            self.level_2_tag = annotation_info[4]
        else:
            self.level_1_entity = "_"
            self.level_2_entity = "_"
            self.level_1_tag = "_"
            self.level_2_tag = "_"
