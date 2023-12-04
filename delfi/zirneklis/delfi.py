import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DelfiZirneklis(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['delfi.lv']
    start_list = []
    # 1200 ziņas => 30 raksti iekš lapas * 40 lapas.
    # Nosakam kur gribam doties minimālo datu ieguvei pirms ievācam kategorijas rakstus mazāk kontrolētā veidā
    for i in range(1,40):
        start_list.append('https://www.delfi.lv/193/politics?page=%d' % i)
        start_list.append('https://www.delfi.lv/auto/42826658/zinas?page=%d' % i)
        start_list.append('https://www.delfi.lv/161/criminal?page=%d' % i)
        start_list.append('https://www.delfi.lv/bizness/44467736/tehnologijas?page=%d' % i)
        start_list.append('https://www.delfi.lv/bizness/37293360/bankas_un_finanses?page=%d' % i)
        start_list.append('https://www.delfi.lv/kultura/174/music?page=%d' % i)
        start_list.append('https://www.delfi.lv/kultura/52862727/screen?page=%d' % i)
        start_list.append('https://www.delfi.lv/life/56017218/atputa?page=%d' % i)
        start_list.append('https://www.delfi.lv/kultura/2094270/books?page=%d' % i)
    for i in range(1,10):
        start_list.append('https://www.delfi.lv/sports/17012608/basketbols?page=%d' % i)
        start_list.append('https://www.delfi.lv/sports/16978259/hokejs?page=%d' % i)
        start_list.append('https://www.delfi.lv/sports/16978250/futbols?page=%d' % i)
        start_list.append('https://www.delfi.lv/sports/19386933/teniss?page=%d' % i)

    start_urls = start_list
    rules = (
        Rule(LinkExtractor(deny='&com|/comments',
                           allow = '.*/sports/.*|.*/auto/42826658/zinas/.*|.*/44467736/tehnologijas/.*|.*/37293360/bankas_un_finanses/.*'
                           +'|.*/193/politics/.*|.*/161/criminal/.*|.*/174/music/.*|.*/52862727/screen/.*'
                           +'|.*/2094270/books/.*|.*/life/56017218/atputa/.*'),
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
            title_extract = r.css('article h1 *::text').get()
            if title_extract:
                title_string = re.sub("\n|\t", "", title_extract)
                title_string = title_string.strip()
            else:
                print('Non-article possibly crawled that did not trigger deny criteria. Title could not be extracted from '
                      + request_url)
                return
        if "Foto:" in title_extract or "Video:" in title_extract:
            print('Foto/Video raksts tiks izlaists: ' + request_url)
            return

        pattern = re.compile('.*delfi.lv\/([^\/]*)\/([^\/]*)\/')
        re_match = pattern.match(request_url)
        category1 = re_match.group(1)
        i['title'] = title_string
        if '/politics/' in request_url:
            i['category'] = 'Politika'
        elif '/auto/' in request_url:
            i['category'] = 'Auto'
        elif '/criminal/' in request_url:
            i['category'] = 'Kriminālziņas'
        elif '/tehnologijas/' in request_url:
            i['category'] = 'Tehnoloģijas'
        elif '/sports/' in request_url:
            i['category'] = 'Sports'
        elif '/bankas_un_finanses/' in request_url:
            i['category'] = 'Finanses'
        elif '/music/' in request_url:
            i['category'] = 'Mūzika'
        elif '/screen/' in request_url:
            i['category'] = 'Kino'
        elif '/atputa/' in request_url:
            i['category'] = 'Atpūta'
        elif '/books/' in request_url:
            i['category'] = 'Literatūra'
        else:            
            i['category'] = category1
        i['body'] = r.css('.article-body-content p::text, .article-body-content a::text, .article-content p::text, '
         +'.article-content div::text, .fragment-lead-text p::text, '
         +'.fragment-paragraph p::text, .fragment-paragraph a::text, .fragment-paragraph strong::text, .fragment-lead-text a::text').extract()
        i['link'] = request_url
        if len(' '.join(i['body']).strip().split()) < 60:
            print('Article of less than 60 words detected under following link. Picture gallery / paid article / broken historic article indicator. '
                      + request_url)
            return
        return i
