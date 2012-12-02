# -*- coding: utf-8 -*-
import os
from pymorphy import get_morph
import lxml.html.clean as clean
from lxml import html
from stop_words import stop_words
import feedparser

class Parse_Text:

    @staticmethod
    def parse(string):
        words_tuple = []
        if string:
            words_tuple = Canonize_Text(string).canonize()
        return words_tuple

class Canonize_Text:
    morphy = get_morph(os.path.join(os.path.dirname(__file__),'dicts', 'ru'))

    def __init__(self, string):
        self.string = string

    def clear_tags(self, string):
        safe_attrs = clean.defs.safe_attrs
        clean.defs.safe_attrs = frozenset()
        cleaner = clean.Cleaner(safe_attrs_only=True)
        try:
            string = cleaner.clean_html(string)
        except ValueError:
            string = ""
        clean.defs.safe_attrs = safe_attrs
        return string

    def canonize(self):
        if self.string:
            return ( [x for x in [self.morphy_process(y.strip(self.get_stop_symbols()))
                                  for y in self.clear_tags(self.string).upper().split()]
                      if x and (x not in self.get_stopwords())] )
        else:
            return ""

    def get_stopwords(self):
        return stop_words

    def get_stop_symbols(self):
        return '.,!?:;-\n\r()'

    def morphy_process(self, string):
        return self.morphy.normalize(string)

class Source_Parser:
    '''
    Родительский класс, от которого наследуем классы конкретных источников
    Получает адрес страницы, достаёт текст новости
    '''
    def __init__(self, url):
        self.url = url

    def parse_rss(self):
        d = feedparser.parse(self.url)
        return d.entries

    def parse_news(self):
        news_data = []

        try:
            for news in self.parse_rss():
                news_data.append({'title': news.title,
                                  'url': news.link,
                                  'content': self.get_news_content(news),
                                  'created': news.published
                })
        except ValueError:
            pass

        return news_data

    def get_news_content(self, news):
        return html.parse(news.link).xpath('//body')[0].text_content()

class Parser_Provider:

    @staticmethod
    def get_parser(source):
        result = {
             'cnews.ru': Cnews_Parser,
             'comnews.ru': Comnews_Parser,
             'digit.ru': Digit_Parser,
             'nag.ru': Nag_Parser,
             'tasstelecom.ru': Tasstelecom_Parser,
             'fiercewireless.com': Fiercewireless_Parser,
             'gigaom.com': Gigaom_Parser,
         }
        return result[source]

class Cnews_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Comnews_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Digit_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Nag_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Tasstelecom_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Fiercewireless_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description

class Gigaom_Parser(Source_Parser):
    def get_news_content(self, news):
        return news.description
