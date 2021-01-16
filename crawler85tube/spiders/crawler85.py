import scrapy
import pymysql

class Crawler85Spider(scrapy.Spider):
    name = 'crawler85'
    allowed_domains = ['85tube.net']

    db = pymysql.connect(
            host="localhost",
            port=8889,
            user="root",
            password="root",
            database="pythondb"
            )
    
    cursor = db.cursor()
    cursortwo = db.cursor()
    
    cursor.execute("SELECT VideoID FROM spider_85tube ORDER BY VideoID DESC")
    cursortwo.execute("SELECT videoPage FROM spider_85tube ORDER BY videoPage")
    
    #get lastid and lastidpage from db
    lastid = cursor.fetchone()
    lastidpage = cursortwo.fetchone()
    
    lastidstr =  ''.join(lastid)
    lastidpagestr =  ''.join(lastidpage)
    
    #take lastidpage and insert into starturls to crawl
    if lastidpagestr:
        stackid = int(lastidpagestr) - 1
        stackidtwo = int(lastidpagestr) + 1
        
    
    start_urls = ['https://85tube.net/latest-updates/%s/' % stackid,
                  'https://85tube.net/latest-updates/%s/' % int(lastidpagestr),
                  'https://85tube.net/latest-updates/%s/' % stackidtwo]
    
    ifLastIdFound = ''
    
    def parse(self, response):
        #loop to check lastid is which page
        if self.ifLastIdFound == '':
            wrapper = response.xpath('//div[@id="list_videos_latest_videos_list"]')
            for wrapperindex in wrapper:
                videos = wrapperindex.xpath('//div[@class="item  "]')
                for video in videos:
                    videoid = video.xpath('.//span[@class="ico-fav-0 "]/@data-fav-video-id').get()
                    #do a callback to parse_video to know current page of videoid
                    videospage = wrapperindex.xpath('.//div[@class="pagination-holder"]//li[@class="page-current"]/span/text()').get()
                    #if found then break loop
                    if videoid in self.lastid:
                        self.ifLastIdFound = True 
                        break
                        return videoid not in self.lastid
                    
                    #follow into link to crawl after break loop
                    link = video.xpath('.//a/@href').get()
                    yield response.follow(url=link, callback=self.parse_video, cb_kwargs=dict(current_page=videospage))
    
    def parse_video(self, response, current_page):        
        #format videoid into embedURL
        video_id = response.xpath('//div[@class="button-group"]/input[2]/@value').get()
        txt = 'https://85tube.net/embed/{}/'
        
        yield {
            'VideoID': response.xpath('//div[@class="button-group"]/input[2]/@value').get(),
            'title': response.xpath('//h1/text()').get(),
            'Duration': response.xpath('//span[contains(text(),"時間: ")][1]/em/text()').get(),
            'tags': response.xpath('//div[contains(text(),"標簽:") or contains(text(),"分類:")]/a/text()').getall(),
            'img_src': response.xpath('//div[@class="block-screenshots"]/a[1]/@href').get(),
            'EmbedURL': txt.format(video_id),
            'videoPage': current_page
            }
