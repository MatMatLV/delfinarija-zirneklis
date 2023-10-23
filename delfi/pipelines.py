import re

class RakstuApstrade(object):
    @staticmethod
    def process_item(item, spider):
        for i, s in enumerate(item['body']):
             item['body'][i] = re.sub("\n|\t", "", s)
        item['body'] = ' '.join(item['body']).strip()
        return item
