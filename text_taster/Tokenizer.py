# *-* coding: UTF-8 -*-
import re


def study_set(filename):
    pass

def to_unicode(word, default=None):
    if not word:
        return default
    if isinstance(word, unicode):
        return word
    elif isinstance(word, list) or isinstance(word, tuple):
        return map(lambda x: to_unicode(x) ,word)
    elif isinstance(word, dict):
        raise AttributeError("sorry!!! toUnicode() is not support 'dict' type.")
    else:
        return unicode(word)


def _replace_tag(text=""):
    text = re.sub(ur"^[0-9]+원$", "#__원__#", text)
    text = re.sub(ur"^[0-9]+x[0-9]+", "#__numXnum__#", text)
    text = re.sub(ur"^[0-9]+세트", "#__세트__#", text)
    text = re.sub(ur"^[0-9]+년$", "#__년__#", text)
    text = re.sub(ur"^[0-9]+ghz$", "#__ghz__#", text)
    text = re.sub(ur"^[0-9]+hz$", "#__hz__#", text)
    text = re.sub(ur"^[0-9]+kg$", "#__kg__#", text)
    text = re.sub(ur"^[0-9]+mg$", "#__mg__#", text)
    text = re.sub(ur"^[0-9]+벌$", "#__벌__#", text)
    text = re.sub(ur"^[0-9]+개$", "#__개__#", text)
    text = re.sub(ur"^[0-9]+매$", "#__매__#", text)
    text = re.sub(ur"^[0-9]+ea$", "#__ea__#", text)
    text = re.sub(ur"^[0-9]+ml$", "#__ml__#", text)
    text = re.sub(ur"^[0-9]+봉$", "#__봉__#", text)
    text = re.sub(ur"^[0-9]+입$", "#__입__#", text)
    text = re.sub(ur"^[0-9]+hz", "#__hz__#", text)
    text = re.sub(ur"^[0-9]+종$", "#__종__#", text)
    text = re.sub(ur"^[0-9]+중$", "#__중__#", text)
    text = re.sub(ur"^[0-9]+병$", "#__병__#", text)
    text = re.sub(ur"^[0-9]+롤$", "#__롤__#", text)
    text = re.sub(ur"^[0-9]+단$", "#__단__#", text)
    text = re.sub(ur"^[0-9]+과$", "#__과__#", text)
    text = re.sub(ur"^[0-9]+g$", "#__g__#", text)
    text = re.sub(ur"^[0-9]+$", "#__number__#", text)
    text = re.sub(ur"^[0-9]+m$", "#__m__#", text)
    text = re.sub(ur"^[0-9a-zA-z]$", "#__char__#", text)
    return text

def stop_filter(s, stop={}):
    if s in stop:
        return None
    for sw in stop:
        if s.startswith(sw) and len(sw)>2:
            s = s[len(sw):]
    return s



class Tokenizer:
    def __init__(self):
        self.delimiter_map = {}
        self.stop = {}

    def _normalize(self, s):
        s =  to_unicode(s)
        s = s.lower()
        s = _replace_tag(s)
        return s

    def add_stop(self, s):
        self.stop[self._normalize(s)] = True

    def del_stop(self, s):
        deli = self._normalize(s)
        if deli in self.delimiter_map:
            del self.stop[deli]

    def add_delimiter(self, s):
        s = to_unicode(s)
        self.delimiter_map[s] = True

    def del_delimiter(self, s):
        deli = self._normalize(s)
        if deli in self.delimiter_map:
            del self.delimiter_map[deli]

    def __call__(self, text):
        if not text:
            yield ""
            return
        text = self._normalize(text)
        temp = u""
        for token in text.split(): # line
            for ch in token: # char
                if ch in self.delimiter_map:
                    if len(temp) > 0:
                        temp = self._normalize(temp)
                        if not temp in self.stop:
                            yield temp
                    temp = u""
                else:
                    temp += ch
            if len(temp) > 0:
                temp = self._normalize(temp)
                if not temp in self.stop:
                    yield temp
                temp  = u""

        if len(temp)>0:
            temp = self._normalize(temp)
            if not temp in self.stop:
                yield temp




