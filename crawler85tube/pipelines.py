# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class Crawler85TubePipeline(object):
    
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host = 'localhost',
            port = 8889,
            user = 'root',
            password = 'root',
            database = 'pythondb'
            )       
        self.c = self.connection.cursor()

        
    def close_spider(self, spider):
        self.connection.close()
    
    
    def process_item(self, item, spider):
        
        def formatDict(dictionary):
            return '{"cn":"%s","en":"","jp":""}' % (dictionary)
        
        def formatStr(string):
            return '"%s"' % (string)
        
        def formatFor(arr):
                reformat = '[';
                index = 0;
                for x in arr:
                    index += 1;

                    if (index == len(arr)):
                        reformat = reformat + '{"cn":"%s","en":"","jp":""}' % (x);
                    else:
                        reformat = reformat + '{"cn":"%s","en":"","jp":""},' % (x);
                return reformat + ']';
          
    
        self.c.execute('''
            INSERT INTO spider_85tube (VideoID,ChineseName,Duration,Tags,ImgURL,EmbedURL,videoPage) VALUES (%s,%s,%s,%s,%s,%s,%s)
            ''', (
            item.get('VideoID'),
            formatDict(item.get('title')),
            item.get('Duration'),
            formatFor(item.get('tags')),
            formatStr(item.get('img_src')),
            formatStr(item.get('EmbedURL')),
            item.get('videoPage')
            ))
        self.connection.commit()
        return item
