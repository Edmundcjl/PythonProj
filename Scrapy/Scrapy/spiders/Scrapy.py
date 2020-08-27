import requests
import scrapy


class Spiders(scrapy.Spider):
    name = "winston"
    allowed_domains = ['192.168.111.129']
    start_urls = ['http://192.168.111.129/index.php']

    def start_requests(self):
        urls = ['http://192.168.111.129/index.php']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'Response.json'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


x = requests.get('http://192.168.111.129/index.php')

p = x.status_code == requests.codes.ok

if p:
    print('Status_OK')
    print(x.status_code)

else:
    print("Failed")

h = {"User-Agent": "Mobile"}
r = requests.get("http://192.168.111.129/headers.php", headers=h)
print(r.text)


class ImgSpiders(scrapy.Spider):
    name = "img"
    allowed_domains = ['http://192.168.111.129/varsity/']
    start_urls = ['http://192.168.111.129/varsity/']

    def start_requests(self):
        urls = [
            'http://192.168.111.129/varsity/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pictures = response.xpath('//img/@src').extract()
        print(pictures)
        xpath_selector = '//img'
        for x in response.xpath(xpath_selector):
            newsel = '@src'
            yield {
                'Image Link': x.xpath(newsel).extract_first(),
            }

            page_selector = '.next a ::attr(href)'
            next_page = response.css(page_selector).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )
