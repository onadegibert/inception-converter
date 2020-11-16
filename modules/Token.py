class Token:
    def __init__(self, string, text_string, onset_start):
        self.string = string
        self.text_string = text_string
        self.onset_start = onset_start
        self.onset, self.offset = self.onset_offset()

    def onset_offset(self):
        onset = self.text_string.find(self.string, self.onset_start)
        if len(self.string) == 1 and self.string != '.':
            offset = onset
        else:
            offset = onset + len(self.string)
        return onset, offset
