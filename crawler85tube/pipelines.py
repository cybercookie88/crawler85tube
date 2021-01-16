# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import pymysql

class Crawler85TubePipeline(object):
    
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1qaz@WSX_OVP",
            database="ovp-project"
            )       
        self.c = self.connection.cursor()

        
    def close_spider(self, spider):
        self.connection.close()
    
    
    def process_item(self, item, spider):
        currentdate = datetime.today().strftime('%Y-%m-%d')

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
            INSERT INTO temp_videos (video_type,title,models,videos_duration,tags,download_link,trailer,img_src,embed_link)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (
            4,
            formatDict(item.get('ChineseName')),
            '[]',
            formatStr(item.get('Duration')),
            formatFor(item.get('Tags')),
            '[]',
            '""',
            formatStr(item.get('ImgURL')),
            formatStr(item.get('EmbedURL'))
            ))

        self.c.execute('''
            INSERT IGNORE INTO clawer_last_videos_detail (video_id, video_ref, video_type, page) VALUES
            (%s, %s, %s, %s)
        ''', (
            item.get('VideoID'),
            currentdate,
            4,
            item.get('videoPage')
        ))

        self.connection.commit()
        return item
