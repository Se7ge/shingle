# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import CONNECT_STRING
from parser import *
from shingle import Shingles

Base = declarative_base()

class News_Sources(Base):
    __tablename__ = 'news_sources'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    rss_url = Column(String)

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    active = Column(SmallInteger(1))
    url = Column(String)
    source_id = Column(Integer, ForeignKey('news_sources.id'))
    created = Column(DateTime)

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.content = kwargs['content']
        self.url = kwargs['url']
        self.source_id = kwargs['source_id']
        self.created = kwargs['created']

class News_Shingles(Base):
    __tablename__ = 'news_shingles'

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    crc32_hash = Column(Integer)

    def __init__(self, news_id, crc32_hash):
        self.news_id = news_id
        self.crc32_hash = crc32_hash

    def __repr__(self):
        return "<News_Shingles('%s','%s')>" % (self.news.title, self.crc32_hash)

class News_Keywords(Base):
    __tablename__ = 'news_keywords'

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    keyword = Column(String)
    crc32_hash = Column(Integer)
    number = Column(Integer)

    def __init__(self, news_id, keyword, crc32_hash, number):
        self.news_id = news_id
        self.keyword = keyword
        self.crc32_hash = crc32_hash
        self.number = number

    def __repr__(self):
        return "<News_Keywords('%s','%s','%s')>" % (self.news.title, self.keyword, self.number)

class Data_Worker:

    def __init__(self):
        self.engine = create_engine(CONNECT_STRING, convert_unicode=True)
        self.engine.execute("SET NAMES utf8")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_sources(self):
        return self.session.query(News_Sources)

    def insert_news(self, news):
        cur_news = News(**news)
        try:
            self.session.add(cur_news)
        except:
            self.session.rollback()
        else:
            self.session.commit()

        return cur_news.id

    def insert_shingles(self, news_id, shingles):
        try:
#            TODO: self.session.add_all()
            for shingle in shingles:
                self.session.add(News_Shingles(news_id, shingle))
        except:
            self.session.rollback()
        else:
            self.session.commit()

    def run_import(self):
        for source in self.get_sources():
            try:
                _parser_class = Parser_Provider.get_parser(source.name)
                _parser = _parser_class(source.rss_url)
                for news in _parser.parse_news():
                    if news['content']:
                        news_words = Parse_Text.parse(news['content'])
                        shingles = Shingles.generate(news['content'])
                        news['source_id'] = source.id
                        news_id = self.insert_news(news)
                        if news_id:
                            self.insert_shingles(news_id, shingles)
            except ValueError:
                pass

