import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DelfiZirneklis(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['delfi.lv']
    start_urls = ['''https://www.delfi.lv/izklaide/",'https://www.delfi.lv/sports/',
     'https://www.delfi.lv/bizness/', 'https://www.delfi.lv/news/national/politics',
     'https://www.delfi.lv/news/national/criminal/''']
    rules = (
        Rule(LinkExtractor(deny='&com|/comments',
                           allow = '''.*/sports/.*|.*/izklaide/.*|.*/bizness/.*|
                            .*/news/national/politics/.*|.*/news/national/criminal/.*''', ),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, r):
        i = {}
        request_url = r.request.url
        title_extract = r.css('.article-title h1 *::text').get()
        if title_extract:
            title_string = re.sub("\n|\t", "", title_extract)
            title_string = title_string.strip()
        else:
            title_extract = r.css('art icle h1 *::text').get()
            if title_extract:
                title_string = re.sub("\n|\t", "", title_extract)
                title_string = title_string.strip()
            else:
                print('Non-article possibly crawled that did not trigger deny criteria. Title could not be extracted from '
                      + request_url)
                return
        pattern = re.compile('.*delfi.lv\/([^\/]*)\/([^\/]*)\/')
        re_match = pattern.match(request_url)
        category1 = re_match.group(1)
        i['title'] = title_string
        if '/politics/' in request_url:
            i['category'] = 'Politics'
        elif '/criminal/' in request_url:
            i['category'] = 'Criminal'
        else:            
            i['category'] = category1
        i['body'] = r.css('''.article-body-content p::text, .article-body-content a::text, .article-content p::text,
         .article-content div::text, .fragment-lead-text p::text, .fragment-paragraph p::text,
             .fragment-paragraph a::text, .fragment-lead-text a::text''').extract()
        i['link'] = request_url
        return i
