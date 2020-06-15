import random
import argparse
import requests
import re

parser = argparse.ArgumentParser(description='Searches Google For Linkedin Profiles')
parser.add_argument('--keyword', type=str, help='keywords to search')
parser.add_argument('--limit', type=int, help='how many profiles to scrape')
args = parser.parse_args()

class LinkedinScraper(object):
    def __init__(self, keyword, limit):
        """

        :param keyword: a str of keyword(s) to search for
        :param limit: number of profiles to scrape
        """
        self.keyword = keyword.replace(' ', '%20')
        self.all_htmls = ""
        self.server = 'www.google.com'
        self.quantity = '100'
        self.limit = int(limit)
        self.counter = 0

    def search(self):
        """
        perform the search
        :return: a list of htmls from Google Searches
        """

        # choose a random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00'
        ]
        while self.counter < self.limit:
            headers = {'User-Agent': random.choice(user_agents)}
            url = 'http://google.com/search?num=100&start=' + str(self.counter) + '&hl=en&meta=&q=site%3Alinkedin.com/in%20' + self.keyword
            resp = requests.get(url, headers=headers)
            if ("Our systems have detected unusual traffic from your computer network.") in resp.text:
                print("Running into captchas")
                return

            self.all_htmls += resp.text
            self.counter += 100

    def parse_links(self):
        reg_links = re.compile(r"url=https:\/\/www\.linkedin.com(.*?)&")
        self.temp = reg_links.findall(self.all_htmls)
        results = []
        for regex in self.temp:
            final_url = regex.replace("url=", "")
            results.append("https://www.linkedin.com" + final_url)
        return results

    def parse_people(self):
        """

        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        reg_people = re.compile(r'">[a-zA-Z0-9._ -]* -|\| LinkedIn')
        self.temp = reg_people.findall(self.all_htmls)
        print(self.temp)
        results = []
        for iteration in (self.temp):
            delete = iteration.replace(' | LinkedIn', '')
            delete = delete.replace(' - LinkedIn', '')
            delete = delete.replace(' profiles ', '')
            delete = delete.replace('LinkedIn', '')
            delete = delete.replace('"', '')
            delete = delete.replace('>', '')
            delete = delete.strip("-")
            if delete != " ":
                results.append(delete)
        return results

if __name__ == "__main__":
    ls = LinkedinScraper(keyword=args.keyword,limit=args.limit)
    ls.search()
    links = ls.parse_links()
    print(links)
    profiles = ls.parse_people()
    print(profiles)