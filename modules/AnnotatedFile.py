import re
import os


def read_gazetteers():
    # Create a dictionary that stores all gazetteers
    gazetteers = dict()
    for file in os.listdir("gazetteers"):
        filename = file.replace('.txt', '')
        with open('gazetteers/' + file, 'r') as f:
            gazetteers[filename] = f.read().splitlines()
    return gazetteers


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
        if '﻿' in text[0]:
            text[0] = re.sub('(  )?<TEXT><!\[CDATA\[﻿', ' ', text[0])
        else:
            text[0] = re.sub('(  )?<TEXT><!\[CDATA\[', '', text[0])
        text_string = ''.join(text)
        return text, text_string

    def clean_tags(self):
        # Read the stored gazetteers
        gazetteers = read_gazetteers()
        tags_in = self.content.index("  <TAGS>\n")
        tags_end = self.content.index("  </TAGS>\n")
        tags = self.content[tags_in + 1:tags_end]
        clean_tags = [line.replace("    ", "") for line in tags]
        last_tag = Tag('<none id="" start="0" end="0" text="" TYPE="none" comment=""/>')
        parsed_tags = [last_tag]
        for each_tag in clean_tags:
            parsed_tag = Tag(each_tag)
            # Discard none tags at both levels
            if parsed_tag.level_1 == "none" and parsed_tag.level_2 == "none":
                continue
            # Process date tag
            if parsed_tag.level_1 == "DATE":
                # Parse standard abbreviation dates
                if re.match('([0-9]{,2}[\/-]){2}[0-9]{2,4}$', parsed_tag.string):
                    parsed_tag.level_2 = "standard abbreviation"
                months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
                          "octubre", "noviembre", "diciembre"]
                # Parse months
                if re.search('|'.join(months), parsed_tag.string.lower()):
                    parsed_tag.level_2 = "month"
                    # Check if there's days and years
                    if re.search('[0-9]{2,4}$', parsed_tag.string):
                        if re.match('[0123][0-9]',parsed_tag.string):
                            days = re.findall('^[0123][0-9]',parsed_tag.string)
                            parsed_tag_day_offset = parsed_tag.onset + len(days[0])
                            parsed_tag_day = Tag(
                                ['', parsed_tag.level_1, "", parsed_tag.onset, parsed_tag_day_offset, days[0],
                                 "day"])
                            parsed_tags.append(parsed_tag_day)
                            year = re.findall('[0-9]{2,4}', parsed_tag.string)[1]
                        else:
                            year = re.findall('[0-9]{2,4}', parsed_tag.string)[0]
                        months = re.findall('|'.join(months), parsed_tag.string)
                        stopwords = ["y", "de", "del", "-"]
                        # TODO Working but level_2 none should be dropped
                        for month in months:
                            parsed_tag_month_onset = re.search(month, parsed_tag.string).start() + parsed_tag.onset
                            parsed_tag_month_offset = parsed_tag_month_onset + len(month)
                            parsed_tag_month = Tag(
                                ['', parsed_tag.level_1, "", parsed_tag_month_onset, parsed_tag_month_offset, month,
                                 "month"])
                            parsed_tags.append(parsed_tag_month)
                        if re.search('|'.join(stopwords), parsed_tag.string):
                            for word in re.findall('|'.join(stopwords), parsed_tag.string):
                                parsed_tag_word_onset = re.search(word, parsed_tag.string).start() + parsed_tag.onset
                                parsed_tag.string = parsed_tag.string.replace(word,'xx',1) #replace word to get next occurrence
                                parsed_tag_word_offset = parsed_tag_word_onset + len(word)
                                parsed_tag_stopword = Tag(
                                    ['', parsed_tag.level_1, '', parsed_tag_word_onset, parsed_tag_word_offset, word,
                                     "none"])
                                parsed_tags.append(parsed_tag_stopword)
                        parsed_tag_year_onset = re.search(year, parsed_tag.string).start() + parsed_tag.onset
                        parsed_tag_year = Tag(
                            ['', parsed_tag.level_1, "", parsed_tag_year_onset, parsed_tag.offset, year,
                             "year"])
                        parsed_tag = parsed_tag_year
                # Parse years
                if re.match("^(año )?[0-9]{4}$", parsed_tag.string):
                    parsed_tag.level_2 = "year"
                    if "año" in parsed_tag.string:
                        parsed_tag.string = parsed_tag.string.replace("año ", "")
                        parsed_tag.onset = parsed_tag.onset + len("año") + 1

            # process territory tag
            if parsed_tag.level_1 == "ADDRESS" and parsed_tag.level_2 == "territory":
                if re.match("(?=.*[a-z])(?=.*[A-Z]).*", parsed_tag.string):
                    if parsed_tag.string in gazetteers['spanish_cities']:
                        parsed_tag.level_2 = "city"
                        if parsed_tag.string in gazetteers['spanish_territories'] and last_tag.level_2 == "city":
                            parsed_tag.level_2 = "territory"
                if re.match("^[0-9]*$", parsed_tag.string):
                    parsed_tag.level_2 = "postcode"
            # Process person tag
            if parsed_tag.level_1 == "PERSON":
                # Parse given name and family name in two separate entities
                if last_tag.level_1 == "PERSON" and last_tag.level_2 == "other:name" and len(
                        parsed_tag.string.split(" ")) > 1:
                    parsed_tag.level_2 = "family name"
                    last_tag.level_2 = "given name"
                    index = parsed_tags.index(last_tag)
                    parsed_tags[index] = last_tag
                # Split one person entity into given and family name
                elif parsed_tag.level_2 == "other:name" and len(parsed_tag.string.split()) > 1:
                    if len(parsed_tag.string.split()) > 3:
                        given_name = ' '.join(parsed_tag.string.split()[:2])
                        family_name = ' '.join(parsed_tag.string.split()[2:])
                    else:
                        given_name = parsed_tag.string.split()[0]
                        family_name = ' '.join(parsed_tag.string.split()[1:])

                    # Process given name entity
                    parsed_tag_given_name_offset = parsed_tag.onset + len(given_name)
                    parsed_tag_given_name = Tag(
                        ['', parsed_tag.level_1, "", parsed_tag.onset, parsed_tag_given_name_offset, given_name,
                         "given name"])
                    parsed_tags.append(parsed_tag_given_name)

                    # Process family name entity
                    parsed_tag_family_name_onset = parsed_tag_given_name.offset + 1
                    parsed_tag_family_name = Tag(
                        ['', parsed_tag.level_1, "", parsed_tag_family_name_onset, parsed_tag.offset, family_name,
                         "family name"])
                    parsed_tag = parsed_tag_family_name
            parsed_tags.append(parsed_tag)
            last_tag = parsed_tag
        return parsed_tags


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
        # TODO Ignore none tags
        return parsed_tag[1], parsed_tag[2].replace('T', ''), int(parsed_tag[3]), int(parsed_tag[4]), parsed_tag[5], \
               parsed_tag[6]
