import scrapy
import pymysql

class Crawler85Spider(scrapy.Spider):
    name = 'crawler85'
    allowed_domains = ['85tube.net']

    db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1qaz@WSX_OVP",
            database="ovp-project"
            )
    
    cursor = db.cursor()

    cursor.execute("SELECT video_id, page FROM clawer_last_videos_detail WHERE video_type = 4 ORDER BY video_id DESC")

    dbResult = cursor.fetchone()

    #get lastid and lastidpage from db
    lastid = dbResult[0]
    lastidpage = dbResult[1]

    lastidstr =  ''.join(lastid)
    lastidpagestr =  ''.join(lastidpage)

    # take lastidpage and insert into starturls to crawl
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
            'ChineseName': response.xpath('//h1/text()').get(),
            'Duration': response.xpath('//span[contains(text(),"時間: ")][1]/em/text()').get(),
            'Tags': response.xpath('//div[contains(text(),"標簽:") or contains(text(),"分類:")]/a/text()').getall(),
            'ImgURL': response.xpath('//div[@class="block-screenshots"]/a[1]/@href').get(),
            'EmbedURL': txt.format(video_id),
            'videoPage': current_page
            }
