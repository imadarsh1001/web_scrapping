# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import pdb

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['www.class-central.com']
    start_urls = ['http://www.class-central.com/subjects']

    def __init__(self,subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:            
            subject_url= response.xpath("//*[contains(@title,'" + self.subject + "')]/@href").extract_first()
            yield Request(response.urljoin(subject_url),callback=self.parse_subject)
        else:
            self.logger.info('scrapping all subjects')
            subjects_url=response.xpath('//*[@class="block"]/@href').extract()
            for subject in subjects_url:
                yield Request(response.urljoin(subject),callback=self.parse_subject)       
    
    def parse_subject(self,response):
        subject_name=response.xpath('//title/text()')[0].extract().split(' | ')[0]
        courses=response.xpath('//*[contains(@class,"course-name-text")]/..')
        for course in courses:
            course_name=course.xpath('.//@title')[0].extract()
            course_url=course.xpath('.//@href')[0].extract()
            absolute_url=response.urljoin(course_url)

            yield {
                'subject_name':subject_name,
                'course_name':course_name,
                'url':absolute_url
            }
    
        next_page=response.xpath('//*[@rel="next"]/@href').extract_first()
        absolute_next_url=response.urljoin(next_page)
        yield Request(absolute_next_url,callback=self.parse_subject)