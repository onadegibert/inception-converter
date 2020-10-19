import re


class AnnotatedFile:
    def __init__(self, filename):
        self.filename = filename
        self.content = self.read_content()
        self.text, self.text_string, self.tags = self.parse_content()

    def read_content(self):
        content = open(self.filename, 'r').readlines()
        return content

    def parse_content(self):
        clean_text, text_string = self.clean_text()
        clean_tags = self.clean_tags()
        return clean_text, text_string, clean_tags

    def clean_text(self):
        text_end = self.content.index("]]></TEXT>\n")
        text = self.content[2:text_end]
        clean_text = [line.strip().replace("<TEXT><![CDATA[", "") for line in text]
        text_string = '\n'.join(clean_text)
        return clean_text, text_string

    def clean_tags(self):
        tags_in = self.content.index("  <TAGS>\n")
        tags_end = self.content.index("  </TAGS>\n")
        tags = self.content[tags_in + 1:tags_end]
        clean_tags = [line.replace("    ", "") for line in tags]
        parsed_tags = list()
        for each_tag in clean_tags:
            parsed_tag = Tag(each_tag)
            parsed_tags.append(parsed_tag)
        return parsed_tags


class Tag:
    def __init__(self, tag_info):
        self.tag_info = tag_info
        self.level_1, self.id, self.onset, self.offset, self.string, self.level_2 = self.parse_tag()

    def parse_tag(self):
        keys = [' id="', '" start="', '" end="', '" text="', '" TYPE="', '" comment=','<','>']
        tag_info_list = re.split("|".join(keys), self.tag_info)
        parsed_tag = tag_info_list
        #TODO Ignore none tags
        return parsed_tag[1], parsed_tag[2].replace('T', ''), int(parsed_tag[3]), int(parsed_tag[4]), parsed_tag[5], parsed_tag[6]
