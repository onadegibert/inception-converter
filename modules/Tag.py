import re


class Tag:
    def __init__(self, tag_info):
        self.tag_info = tag_info
        self.level_1, self.id, self.onset, self.offset, self.string, self.level_2 = self.parse_tag()

    def parse_tag(self):
        keys = [' id="', '" start="', '" end="', '" text="', '" TYPE="', '" comment=', '<', '>']
        # Process input (it can be in string format or, already in a list)
        if type(self.tag_info) == str:
            tag_info_list = re.split("|".join(keys), self.tag_info)
            parsed_tag = tag_info_list
        else:
            parsed_tag = self.tag_info
        return parsed_tag[1], parsed_tag[2].replace('T', ''), int(parsed_tag[3]), int(parsed_tag[4]), parsed_tag[5], \
               parsed_tag[6]
